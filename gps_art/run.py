"""End-to-end: search every candidate area for every shape, keep the best
placements, write GPX / PNG / HTML and a summary.

    python -m gps_art.run [--shapes FOTINI,LOVE,heart] [--areas Pimlico,...]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import pickle
import time

import numpy as np

from . import areas as A
from . import export as X
from . import search as S
from . import shapes as SH
from .streets import StreetNet, download

OUT = os.path.join(os.path.dirname(__file__), "..", "output")

# metres per unit (letter height = 4 units) to try, per shape
UNITS = {
    "FOTINI": [100, 115, 130],
    "LOVE": [120, 135, 150],
    "heart": [220, 300, 380, 460],
    "FOTINI_wide": [95, 110, 125],
    "FOTINI_font": [105, 120, 135],
    "greek_font": [95, 110, 125],
}
THETAS = list(range(-30, 31, 5))


def all_shapes():
    sh = SH.candidate_shapes()
    try:
        f = SH.font_word("FOTINI", name="FOTINI_font")
        sh["FOTINI_font"] = f
    except Exception as e:
        print("Latin font shape failed:", e)
    try:
        g = SH.font_word("Φωτεινή", name="greek_font")
        sh["greek_font"] = g
    except Exception as e:
        print("Greek font shape failed (font lacks glyphs?):", e)
    return sh


def load_net(name):
    lat, lon = A.AREAS[name]
    G, st = download(name, lat, lon, A.RADIUS)
    net = StreetNet.build(name, G, st)
    import pyproj
    tf = pyproj.Transformer.from_crs("EPSG:4326", net.crs, always_xy=True)
    centre = np.array(tf.transform(lon, lat))
    return net, centre


def rotate_loop_to_station(net, pl):
    """For closed shapes, start the loop at the route point closest to a station."""
    R = pl.route_xy
    if np.hypot(*(R[0] - R[-1])) > 1:
        return
    best = (math.inf, 0)
    for i, p in enumerate(R[:-1]):
        st, d = net.nearest_station(p)
        if d < best[0]:
            best = (d, i)
    i = best[1]
    pl.route_xy = np.vstack([R[i:-1], R[:i + 1]])
    # nodes/edges order for problem spots does not matter for a loop
    pl.metrics.update(S.metrics(net, pl.shape_xy, pl.route_xy, pl.unit))
    for k in ("readability", "badness"):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", default="FOTINI,FOTINI_wide,LOVE,heart,FOTINI_font,greek_font")
    ap.add_argument("--areas", default=",".join(A.AREAS))
    ap.add_argument("--keep", type=int, default=30, help="placements routed per area+shape")
    ap.add_argument("--top", type=int, default=3)
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    shapes = all_shapes()
    want = [s for s in args.shapes.split(",") if s in shapes]
    results = {s: [] for s in want}
    nets = {}
    for area in args.areas.split(","):
        t0 = time.time()
        try:
            net, centre = load_net(area)
        except Exception as e:
            print(f"[{area}] unavailable: {e!r}")
            continue
        nets[area] = net
        print(f"[{area}] {len(net.xy)} nodes, {len(net.eu)} edges, {len(net.stations)} stations", flush=True)
        for sname in want:
            shape = shapes[sname]
            cands = S.proxy_search(net, shape, UNITS[sname], THETAS, centre, A.RADIUS, keep=args.keep)
            for pl in cands:
                S.evaluate(net, shape, pl)
            cands = [c for c in cands if math.isfinite(c.score)]
            cands.sort(key=lambda c: c.score)
            for c in cands[:2]:
                print(f"   {sname:12s} u={c.unit:.0f} th={c.theta:+.0f} proxy={c.proxy:.2f} "
                      f"score={c.score:.3f} read={c.metrics['readability']} len={c.metrics['length_km']:.1f}km",
                      flush=True)
            results[sname].extend(cands[:3])
        print(f"[{area}] done in {time.time() - t0:.0f}s", flush=True)

    # refine the global best few per shape and keep top N in distinct areas
    final = {}
    for sname, cands in results.items():
        cands.sort(key=lambda c: c.score)
        picked, areas_used = [], set()
        for c in cands:
            if c.area in areas_used:
                continue
            areas_used.add(c.area)
            picked.append(c)
            if len(picked) >= args.top:
                break
        refined = []
        for c in picked:
            r = S.flex_optimize(nets[c.area], shapes[sname], c) if sname != "heart" else c
            r = S.refine(nets[c.area], shapes[sname], r)
            print(f"refined {sname} {c.area}: {c.score:.3f} -> {r.score:.3f}", flush=True)
            refined.append(r)
        refined.sort(key=lambda c: c.score)
        final[sname] = refined
    with open(os.path.join(OUT, "..", ".cache", "final.pkl"), "wb") as f:
        pickle.dump({k: [(p.area, p.shape, p.unit, p.theta, p.cx, p.cy) for p in v] for k, v in final.items()}, f)
    write_outputs(final, nets, shapes)


def write_outputs(final, nets, shapes):
    rows = []
    for sname, pls in final.items():
        for rank, pl in enumerate(pls, 1):
            net = nets[pl.area]
            if sname == "heart":
                rotate_loop_to_station(net, pl)
            name = f"{sname}_{rank}"
            st, sd = net.nearest_station(pl.route_xy[0])
            st2, sd2 = net.nearest_station(pl.route_xy[-1])
            spots, summ = X.problem_spots(net, pl.nodes, pl.edges)
            wps = [("Start", f"Start near {st[0]} station ({sd:.0f} m)" if st else "Start", pl.route_xy[0]),
                   ("Finish", f"Finish near {st2[0]} station ({sd2:.0f} m)" if st2 else "Finish",
                    pl.route_xy[-1])]
            gpx = os.path.join(OUT, f"route_{name}.gpx")
            X.write_gpx(gpx, f"{sname} GPS art – {pl.area}", pl.route_xy, wps)
            val = X.validate_gpx(gpx, net)
            title = (f"{sname} — {pl.area}: {pl.metrics['length_km']:.1f} km, letters {4 * pl.unit:.0f} m tall, "
                     f"start near {st[0] if st else '?'}")
            X.preview_png(os.path.join(OUT, f"preview_{name}.png"), net, pl, title)
            X.preview_png(os.path.join(OUT, "..", ".cache", f"debug_{name}.png"), net, pl, title, show_target=True)
            X.folium_map(os.path.join(OUT, f"map_{name}.html"), pl, f"{sname} ({pl.area})", spots, st)
            rows.append(dict(name=name, shape=sname, area=pl.area, unit=pl.unit, theta=pl.theta,
                             metrics=pl.metrics, validation=val, spots=spots, spot_summary=summ,
                             start=X.to_latlon(pl.route_xy[:1])[0].tolist(),
                             end=X.to_latlon(pl.route_xy[-1:])[0].tolist(),
                             start_station=(st[0], st[5], sd) if st else None,
                             end_station=(st2[0], st2[5], sd2) if st2 else None))
            print(name, pl.area, json.dumps(val), flush=True)
    with open(os.path.join(OUT, "..", ".cache", "rows.pkl"), "wb") as f:
        pickle.dump(rows, f)
    return rows


if __name__ == "__main__":
    main()


def write_summary(rows, verdicts, path=os.path.join(OUT, "summary.md"), intro=""):
    """verdicts: {name: (legible: bool, note)} — filled in after looking at each preview."""
    L = ["# GPS-art route candidates", "", intro, ""]
    L += ["| Route | Area | Distance | Start (nearest station) | Finish (nearest station) | Readability score | Legible? |",
          "|---|---|---|---|---|---|---|"]
    for r in rows:
        m = r["metrics"]
        v = verdicts.get(r["name"], (None, ""))
        leg = {True: "yes", False: "**no — rejected**", None: "?"}[v[0]]
        st = r["start_station"]; en = r["end_station"]
        L.append(f"| `{r['name']}` | {r['area']} | {r['validation']['gpx_length_km']:.2f} km | "
                 f"{st[0]} ({st[2]:.0f} m) | {en[0]} ({en[2]:.0f} m) | {m['readability']:.0f}/100 | {leg} |")
    L += ["", "Readability score: 100 means the route lies exactly on the drawn letters; it falls as the mean "
          "and 90th-percentile gap between the route and the intended shape grow, measured in stroke units "
          "(1 unit = a quarter of the letter height). Around 60+ usually reads well; below ~45 it rarely does. "
          "The final call is the 'Legible?' column, which comes from looking at each preview.", ""]
    for r in rows:
        m, val = r["metrics"], r["validation"]
        v = verdicts.get(r["name"], (None, ""))
        st, en = r["start_station"], r["end_station"]
        L += [f"## `{r['name']}` — {r['area']}", ""]
        if v[1]:
            L += [f"**Verdict:** {v[1]}", ""]
        L += [f"- Files: `route_{r['name']}.gpx`, `preview_{r['name']}.png`, `map_{r['name']}.html`",
              f"- Distance: **{val['gpx_length_km']:.2f} km** (the drawing itself is {m['shape_km']:.1f} km; "
              f"streets add {100 * (m['detour_ratio'] - 1):.0f}%)",
              f"- Letter height: about {m['letter_height_m']:.0f} m; rotation {r['theta']:+.0f}° (positive = counter-clockwise)",
              f"- Start: {r['start'][0]:.5f}, {r['start'][1]:.5f} — nearest station **{st[0]}** "
              f"({st[1] or 'station'}), {st[2]:.0f} m away in a straight line",
              f"- Finish: {r['end'][0]:.5f}, {r['end'][1]:.5f} — nearest station **{en[0]}**, {en[2]:.0f} m away",
              f"- Fit: mean gap shape→route {m['mean_shape_to_route']:.0f} m, route→shape {m['mean_route_to_shape']:.0f} m; "
              f"90th percentile {max(m['p90_shape_to_route'], m['p90_route_to_shape']):.0f} m; worst {m['hausdorff']:.0f} m",
              f"- Readability score: {m['readability']:.0f}/100",
              f"- GPX check: {val['points']} points, {val['gpx_length_km']:.2f} km, largest gap between points "
              f"{val['max_step_m']:.1f} m (jumps > 30 m: {val['jumps']}), furthest point from a walkable street "
              f"{val['max_off_edge_m']:.1f} m ({val['off_edge_points']} points > 3 m) → "
              f"{'**passed**' if val['ok'] else '**FAILED**'}", ""]
        spots, summ = r["spots"], r["spot_summary"]
        L.append("Problem spots:")
        cross = [t for k, t, _ in spots if k == "crossing"]
        if cross:
            from collections import Counter
            cc = Counter(cross)
            L.append("- Crossings of main roads (use the signalled crossing; GPS keeps drawing while you wait): "
                     + "; ".join(f"{t}" + (f" ×{n}" if n > 1 else "") for t, n in cc.most_common()))
        for kind, label in (("bridge", "Bridges"), ("tunnel", "Tunnels/underpasses"), ("steps", "Steps")):
            items = sorted({t for k, t, _ in spots if k == kind})
            if items:
                L.append(f"- {label}: " + "; ".join(items))
        if summ["major"]:
            L.append("- Along main roads (pavement, busy): " + ", ".join(f"{n} ({l} m)" for n, l in summ["major"][:6]))
        if summ["oneway"]:
            L.append("- One-way for traffic (fine on foot, the pavement is two-way): "
                     + ", ".join(f"{n} ({l} m)" for n, l in summ["oneway"][:8]))
        if summ["paths"]:
            L.append("- Footpaths / park paths (some parks and squares lock at dusk — run in daylight): "
                     + ", ".join(f"{n} ({l} m)" for n, l in summ["paths"][:8]))
        L.append("")
    with open(path, "w") as f:
        f.write("\n".join(L))
