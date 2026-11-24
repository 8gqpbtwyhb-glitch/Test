"""GPX / PNG / folium output, GPX validation and problem-spot detection."""
from __future__ import annotations

import math
from collections import Counter

import gpxpy
import gpxpy.gpx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pyproj
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Point
from shapely.strtree import STRtree

from .shapes import densify
from .streets import MAJOR, UTM, _first

_to_ll = pyproj.Transformer.from_crs(UTM, "EPSG:4326", always_xy=True)
_to_xy = pyproj.Transformer.from_crs("EPSG:4326", UTM, always_xy=True)


def to_latlon(xy):
    lon, lat = _to_ll.transform(xy[:, 0], xy[:, 1])
    return np.c_[lat, lon]


# ------------------------------------------------------------------ GPX
def write_gpx(path, title, route_xy, waypoints, step=10.0):
    """route_xy in metres; waypoints [(name, desc, (x, y))]."""
    pts = densify(route_xy, step)
    # drop consecutive duplicates
    keep = np.r_[True, np.hypot(*np.diff(pts, axis=0).T) > 0.01]
    pts = pts[keep]
    ll = to_latlon(pts)
    g = gpxpy.gpx.GPX()
    g.creator = "gps_art route generator"
    g.name = title
    for nm, desc, p in waypoints:
        lat, lon = to_latlon(np.array([p]))[0]
        g.waypoints.append(gpxpy.gpx.GPXWaypoint(latitude=round(lat, 7), longitude=round(lon, 7),
                                                 name=nm, description=desc))
    trk = gpxpy.gpx.GPXTrack(name=title)
    trk.type = "running"
    seg = gpxpy.gpx.GPXTrackSegment()
    for lat, lon in ll:
        seg.points.append(gpxpy.gpx.GPXTrackPoint(round(lat, 7), round(lon, 7)))
    trk.segments.append(seg)
    g.tracks.append(trk)
    with open(path, "w") as f:
        f.write(g.to_xml(version="1.1"))


def validate_gpx(path, net, max_off_edge=3.0, max_jump=30.0):
    """Reload a GPX and check distance, on-network-ness and jumps."""
    with open(path) as f:
        g = gpxpy.parse(f)
    pts = [(p.latitude, p.longitude) for t in g.tracks for s in t.segments for p in s.points]
    ll = np.array(pts)
    x, y = _to_xy.transform(ll[:, 1], ll[:, 0])
    xy = np.c_[x, y]
    steps = np.hypot(*np.diff(xy, axis=0).T)
    tree = STRtree(net.egeom)
    off = []
    for p in xy:
        P = Point(p)
        j = tree.nearest(P)
        off.append(net.egeom[j].distance(P))
    off = np.array(off)
    res = dict(
        points=len(pts),
        gpx_length_km=g.length_2d() / 1000,
        max_step_m=float(steps.max()),
        jumps=int((steps > max_jump).sum()),
        max_off_edge_m=float(off.max()),
        off_edge_points=int((off > max_off_edge).sum()),
        waypoints=len(g.waypoints),
    )
    res["ok"] = res["jumps"] == 0 and res["off_edge_points"] == 0
    return res


# ------------------------------------------------------------------ problem spots
def problem_spots(net, nodes, edges):
    used = set(edges)
    out = []
    def names(e):
        n = net.etags[e].get("name") or net.etags[e].get("highway")
        return " / ".join(map(str, n)) if isinstance(n, list) else str(n)
    lens = Counter()
    for e in edges:
        t = net.etags[e]
        hw = _first(t.get("highway"))
        if _first(t.get("bridge")) not in (None, "no", False):
            out.append(("bridge", f"{names(e)} (bridge)", net.egeom[e].interpolate(0.5, normalized=True).coords[0]))
        if _first(t.get("tunnel")) not in (None, "no", False):
            out.append(("tunnel", f"{names(e)} (tunnel/underpass, GPS may drop)",
                        net.egeom[e].interpolate(0.5, normalized=True).coords[0]))
        if hw == "steps":
            out.append(("steps", f"steps on {names(e)}", net.egeom[e].interpolate(0.5, normalized=True).coords[0]))
        if t.get("oneway") in (True, "yes", "True") or (isinstance(t.get("oneway"), list) and True in t.get("oneway")):
            lens[("oneway", names(e))] += net.elen[e]
        if hw in ("footway", "path", "pedestrian", "track", "bridleway", "cycleway"):
            lens[("path", names(e))] += net.elen[e]
        if hw in MAJOR:
            lens[("major", names(e))] += net.elen[e]
    # crossings of major roads: route passes a node where a major road meets,
    # but does not run along that road through the node
    adj = {}
    for i, (a, b) in enumerate(zip(net.eu, net.ev)):
        adj.setdefault(a, []).append(i)
        adj.setdefault(b, []).append(i)
    seen_x = set()
    for k in range(1, len(nodes) - 1):
        n = nodes[k]
        major_here = [e for e in adj.get(n, []) if _first(net.etags[e].get("highway")) in MAJOR]
        if not major_here:
            continue
        on_major = any(e in used and e in major_here for e in adj.get(n, []))
        if not on_major or len(major_here) >= 1:
            rn = sorted({str(names(e)) for e in major_here})
            key = (tuple(rn), round(net.xy[n][0] / 60), round(net.xy[n][1] / 60))
            if key in seen_x:
                continue
            seen_x.add(key)
            if not on_major:
                out.append(("crossing", f"cross {', '.join(rn)}", tuple(net.xy[n])))
    # dedupe bridges by name
    dedup, seen = [], set()
    for kind, txt, p in out:
        k2 = (kind, txt) if kind != "crossing" else (kind, txt, round(p[0] / 150), round(p[1] / 150))
        if k2 in seen:
            continue
        seen.add(k2)
        dedup.append((kind, txt, p))
    summary = dict(
        oneway=sorted([(n, round(l)) for (k, n), l in lens.items() if k == "oneway"], key=lambda x: -x[1]),
        paths=sorted([(n, round(l)) for (k, n), l in lens.items() if k == "path"], key=lambda x: -x[1]),
        major=sorted([(n, round(l)) for (k, n), l in lens.items() if k == "major"], key=lambda x: -x[1]),
    )
    return dedup, summary


# ------------------------------------------------------------------ images
def preview_png(path, net, pl, title, show_target=False, pad=250):
    R = pl.route_xy
    lo = R.min(axis=0) - pad
    hi = R.max(axis=0) + pad
    w, h = hi - lo
    fig_w = 14
    fig_h = max(4.5, fig_w * h / w * (2 if not show_target else 1) + 1.2)
    fig, axs = plt.subplots(2, 1, figsize=(fig_w, fig_h), gridspec_kw=dict(height_ratios=[1, 1]))
    for ax, streets in zip(axs, (True, False)):
        if streets:
            # street background (only edges in view)
            inview = np.all((net.xy[net.eu] > lo - 300) & (net.xy[net.eu] < hi + 300), axis=1)
            for e in np.nonzero(inview)[0]:
                c = np.asarray(net.egeom[e].coords)
                hw = _first(net.etags[e].get("highway"))
                lw = 1.6 if hw in MAJOR else 0.7
                col = "#b9b9b9" if hw not in ("footway", "path", "pedestrian", "steps", "track") else "#cfe3c9"
                ax.plot(c[:, 0], c[:, 1], color=col, lw=lw, zorder=1, solid_capstyle="round")
            for nm, x, y, *_ in net.stations:
                if lo[0] - 300 < x < hi[0] + 300 and lo[1] - 300 < y < hi[1] + 300:
                    ax.plot(x, y, "s", color="#1d4ed8", ms=6, zorder=4)
                    ax.annotate(nm, (x, y), xytext=(4, 4), textcoords="offset points", fontsize=7,
                                color="#1d4ed8", zorder=4)
            if show_target:
                ax.plot(pl.shape_xy[:, 0], pl.shape_xy[:, 1], "--", color="#2563eb", lw=1, alpha=0.6, zorder=2)
            ax.set_title(title, fontsize=11)
        else:
            ax.set_title("Same route without the street map (roughly how Strava will show it)", fontsize=9)
        ax.plot(R[:, 0], R[:, 1], color="#fc4c02", lw=3.2 if streets else 4, zorder=3,
                solid_joinstyle="round", solid_capstyle="round")
        ax.plot(*R[0], marker="*", color="#16a34a", ms=18, mec="k", zorder=5)
        ax.plot(*R[-1], marker="o", color="#111", ms=8, zorder=5)
        if streets:
            ax.annotate("START", R[0], xytext=(8, -14), textcoords="offset points", fontsize=9,
                        weight="bold", color="#166534", zorder=6)
            ax.annotate("FINISH", R[-1], xytext=(8, 6), textcoords="offset points", fontsize=8,
                        color="#111", zorder=6)
        ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1])
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        # scale bar
        sb = 500 if w > 1500 else 200
        ax.plot([lo[0] + 60, lo[0] + 60 + sb], [lo[1] + 60] * 2, color="k", lw=2, zorder=6)
        ax.text(lo[0] + 60 + sb / 2, lo[1] + 85, f"{sb} m", ha="center", fontsize=8, zorder=6)
        ax.text(hi[0] - 40, hi[1] - 40, "N ↑", ha="right", va="top", fontsize=10, zorder=6)
    fig.text(0.01, 0.005, "Street data © OpenStreetMap contributors", fontsize=7, color="#666")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def folium_map(path, pl, title, spots, station):
    import folium
    ll = to_latlon(pl.route_xy)
    m = folium.Map(location=ll.mean(axis=0).tolist(), zoom_start=15, tiles="OpenStreetMap",
                   control_scale=True)
    folium.PolyLine(ll.tolist(), color="#fc4c02", weight=5, opacity=0.9, tooltip=title).add_to(m)
    folium.Marker(ll[0].tolist(), tooltip="Start", icon=folium.Icon(color="green", icon="play")).add_to(m)
    folium.Marker(ll[-1].tolist(), tooltip="Finish", icon=folium.Icon(color="black", icon="flag")).add_to(m)
    if station:
        folium.Marker([station[3], station[4]], tooltip=f"{station[0]} station",
                      icon=folium.Icon(color="blue", icon="train", prefix="fa")).add_to(m)
    for kind, txt, p in spots:
        q = to_latlon(np.array([p]))[0]
        folium.CircleMarker(q.tolist(), radius=5, color="#7c3aed", fill=True, tooltip=txt).add_to(m)
    m.fit_bounds([ll.min(axis=0).tolist(), ll.max(axis=0).tolist()])
    m.save(path)


def major_crossings(route_xy, roads_ll):
    """Count where the route crosses (not runs along) a main road. roads_ll from
    pbf.major_roads: [(name, [(lat, lon), ...])]."""
    from collections import Counter
    from shapely.strtree import STRtree
    R = LineString(route_xy)
    lo, hi = route_xy.min(axis=0) - 50, route_xy.max(axis=0) + 50
    geoms, names = [], []
    for nm, pts in roads_ll:
        ll = np.array(pts)
        x, y = _to_xy.transform(ll[:, 1], ll[:, 0])
        if x.max() < lo[0] or x.min() > hi[0] or y.max() < lo[1] or y.min() > hi[1]:
            continue
        geoms.append(LineString(np.c_[x, y])); names.append(nm)
    c = Counter()
    # sample route as short segments; a crossing = segment intersects road but
    # the route is not running alongside it (pavement parallel to road)
    for a, b in zip(route_xy[:-1], route_xy[1:]):
        seg = LineString([a, b])
        if seg.length < 0.5:
            continue
        for g, nm in zip(geoms, names):
            if seg.intersects(g):
                # direction check: crossing if roughly perpendicular (> 35 deg)
                p = g.interpolate(g.project(seg.interpolate(0.5, normalized=True)))
                d = g.interpolate(min(g.length, g.project(p) + 5))
                v1 = np.array(b) - np.array(a)
                v2 = np.array(d.coords[0]) - np.array(p.coords[0])
                if np.linalg.norm(v2) < 1e-6:
                    continue
                cosang = abs(v1 @ v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                if cosang < 0.82:
                    c[nm] += 1
    return c
