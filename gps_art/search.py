"""Search scale / rotation / offset of a shape over a street network."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.spatial import cKDTree

from .shapes import Shape, densify, flexed

LEN_TARGET_KM = 12.0
LEN_MAX_KM = 15.0


@dataclass
class Placement:
    area: str
    shape: str
    unit: float          # metres per shape unit (letter height = 4 units)
    theta: float         # rotation, degrees (counter-clockwise)
    cx: float
    cy: float
    proxy: float = math.inf
    # filled in after routing
    nodes: list = None
    route_xy: np.ndarray = None
    edges: list = None
    shape_xy: np.ndarray = None
    metrics: dict = field(default_factory=dict)
    score: float = math.inf
    flex: dict = field(default_factory=dict)   # per-letter (dx, dy, scale) tweaks, units

    def key(self):
        return (self.area, self.shape, round(self.unit), round(self.theta, 1), round(self.cx), round(self.cy))


def place(pts_units, centre_units, unit, theta, cx, cy):
    t = math.radians(theta)
    R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
    return (pts_units - centre_units) @ R.T * unit + np.array([cx, cy])


def shape_centre(shape: Shape):
    lo, hi = shape.path.min(axis=0), shape.path.max(axis=0)
    return (lo + hi) / 2


def proxy_search(net, shape: Shape, units, thetas, area_centre, radius, step_frac=0.6, keep=12):
    c0 = shape_centre(shape)
    samp = densify(shape.path, 0.25)
    d = np.diff(samp, axis=0)
    keepm = np.hypot(d[:, 0], d[:, 1]) > 1e-9
    samp_pts = samp[:-1][keepm]
    tang_u = np.arctan2(d[keepm, 1], d[keepm, 0])
    results = []
    for unit in units:
        step = step_frac * unit
        for th in thetas:
            local = place(samp_pts, c0, unit, th, 0, 0)
            tang = (tang_u + math.radians(th)) % np.pi
            r_shape = np.max(np.hypot(local[:, 0], local[:, 1]))
            free = radius - 250 - r_shape
            if free <= 0:
                continue
            offs = np.arange(-free, free + 1e-6, step)
            for ox_ in offs:
                for oy_ in offs:
                    if ox_ * ox_ + oy_ * oy_ > free * free:
                        continue
                    pts = local + np.array([area_centre[0] + ox_, area_centre[1] + oy_])
                    cost = net.proxy_cost(pts, tang, unit)
                    results.append((cost, unit, th, area_centre[0] + ox_, area_centre[1] + oy_))
    results.sort(key=lambda r: r[0])
    # non-maximum suppression -> diverse placements
    chosen = []
    for r in results:
        if all(not (abs(r[2] - c[2]) < 8 and abs(r[1] - c[1]) < 1 and
                    math.hypot(r[3] - c[3], r[4] - c[4]) < 3 * r[1]) for c in chosen):
            chosen.append(r)
        if len(chosen) >= keep:
            break
    return [Placement(net.name, shape.name, u, th, x, y, proxy=c) for c, u, th, x, y in chosen]


def waypoints_units(shape: Shape, spacing=2.0, corner_deg=20):
    """Corners of the shape path plus intermediate points every `spacing` units."""
    P = shape.path
    keep = [0]
    for i in range(1, len(P) - 1):
        a, b = P[i] - P[i - 1], P[i + 1] - P[i]
        na, nb = np.hypot(*a), np.hypot(*b)
        if na < 1e-9 or nb < 1e-9:
            continue
        cosang = np.clip(a @ b / (na * nb), -1, 1)
        if math.degrees(math.acos(cosang)) > corner_deg:
            keep.append(i)
    keep.append(len(P) - 1)
    out = [P[keep[0]]]
    for i, j in zip(keep[:-1], keep[1:]):
        seg = P[i:j + 1]
        L = np.hypot(*np.diff(seg, axis=0).T).sum()
        n = max(1, int(round(L / spacing)))
        # walk along the sub-polyline
        cum = np.r_[0, np.cumsum(np.hypot(*np.diff(seg, axis=0).T))]
        for k in range(1, n + 1):
            t = L * k / n
            q = np.searchsorted(cum, t, side="right") - 1
            q = min(q, len(seg) - 2)
            f = (t - cum[q]) / max(cum[q + 1] - cum[q], 1e-9)
            out.append(seg[q] + (seg[q + 1] - seg[q]) * f)
    return np.array(out)


def _poly_len(P):
    return float(np.hypot(*np.diff(P, axis=0).T).sum())


def evaluate(net, shape: Shape, pl: Placement, closed=False):
    c0 = shape_centre(shape)
    shape = flexed(shape, pl.flex)
    spacing = 1.5 if shape.name == "heart" else 2.0
    wp = place(waypoints_units(shape, spacing), c0, pl.unit, pl.theta, pl.cx, pl.cy)
    nodes = net.route(wp, pl.unit)
    if nodes is None:
        pl.score = math.inf
        return pl
    route_xy, edges = net.path_geometry(nodes)
    shape_xy = place(shape.path, c0, pl.unit, pl.theta, pl.cx, pl.cy)
    pl.nodes, pl.route_xy, pl.edges, pl.shape_xy = nodes, route_xy, edges, shape_xy
    pl.metrics = metrics(net, shape_xy, route_xy, pl.unit)
    pl.score = objective(pl.metrics) + 0.04 * sum(abs(dx) + abs(dy) + 3 * abs(sc - 1)
                                                  for dx, dy, sc in pl.flex.values())
    return pl


def metrics(net, shape_xy, route_xy, unit):
    S = densify(shape_xy, 5.0)
    R = densify(route_xy, 5.0)
    dsr, _ = cKDTree(R).query(S)
    drs, _ = cKDTree(S).query(R)
    L = _poly_len(route_xy) / 1000
    m = dict(
        length_km=L,
        shape_km=_poly_len(shape_xy) / 1000,
        mean_shape_to_route=float(dsr.mean()),
        mean_route_to_shape=float(drs.mean()),
        p90_shape_to_route=float(np.percentile(dsr, 90)),
        p90_route_to_shape=float(np.percentile(drs, 90)),
        hausdorff=float(max(dsr.max(), drs.max())),
        unit=unit,
        letter_height_m=4 * unit,
    )
    m["badness"] = ((m["mean_shape_to_route"] + m["mean_route_to_shape"]) / 2
                    + 0.5 * max(m["p90_shape_to_route"], m["p90_route_to_shape"])) / unit
    # "readability": 100 = route lies exactly on the drawing; ~50 = average error
    # of about a third of a stroke unit. Calibrated by eye on the previews.
    m["readability"] = round(100 * math.exp(-1.7 * m["badness"]), 1)
    m["detour_ratio"] = L / max(m["shape_km"], 1e-6)
    st, sd = net.nearest_station(route_xy[0])
    m["start_station"] = st[0] if st else None
    m["start_station_m"] = sd
    st2, sd2 = net.nearest_station(route_xy[-1])
    m["end_station"] = st2[0] if st2 else None
    m["end_station_m"] = sd2
    return m


def objective(m):
    s = m["badness"]
    over = m["length_km"] - LEN_TARGET_KM
    if over > 0:
        s += 0.10 * over
    if m["length_km"] > LEN_MAX_KM:
        s += 1.0 + 0.5 * (m["length_km"] - LEN_MAX_KM)
    s += 0.15 * max(0.0, m["detour_ratio"] - 1.25)
    s += min(0.15, 0.03 * max(0.0, (m["start_station_m"] - 300) / 100))
    return s


def refine(net, shape, pl: Placement, rounds=2):
    """Local search around a routed placement."""
    best = pl
    for r in range(rounds):
        cands = []
        du = best.unit * 0.35 / (r + 1)
        for dx in (-du, 0, du):
            for dy in (-du, 0, du):
                for dth in (-3 / (r + 1), 0, 3 / (r + 1)):
                    for ds in (0.94, 1.0, 1.06):
                        if dx == dy == dth == 0 and ds == 1.0:
                            continue
                        cands.append(Placement(best.area, best.shape, best.unit * ds, best.theta + dth,
                                               best.cx + dx, best.cy + dy, flex=dict(best.flex)))
        rng = np.random.default_rng(r)
        cands = [cands[i] for i in rng.choice(len(cands), size=min(24, len(cands)), replace=False)]
        for c in cands:
            evaluate(net, shape, c)
            if c.score < best.score:
                best = c
    return best


def _copy(pl, **kw):
    q = Placement(pl.area, pl.shape, pl.unit, pl.theta, pl.cx, pl.cy, flex=dict(pl.flex))
    for k, v in kw.items():
        setattr(q, k, v)
    return q


def flex_optimize(net, shape, pl: Placement, passes=2, steps=(-0.5, -0.25, 0, 0.25, 0.5),
                  scales=(0.88, 1.0, 1.12)):
    """Coordinate descent: nudge each letter on its own so it locks onto local
    streets, keeping the word's overall layout."""
    best = pl if pl.nodes is not None else evaluate(net, shape, pl)
    items = sorted(set(shape.item.tolist()))
    for p_ in range(passes):
        improved = False
        for i in items:
            cur = best.flex.get(i, (0.0, 0.0, 1.0))
            trials = [(cur[0] + dx / (p_ + 1), cur[1] + dy / (p_ + 1), cur[2])
                      for dx in steps for dy in steps if dx or dy]
            for t in trials:
                if abs(t[0]) > 0.75 or abs(t[1]) > 0.75:
                    continue
                q = _copy(best); q.flex[i] = t
                evaluate(net, shape, q)
                if q.score < best.score - 1e-4:
                    best, improved = q, True
            cur = best.flex.get(i, (0.0, 0.0, 1.0))
            for sc in scales:
                if sc == 1.0:
                    continue
                q = _copy(best); q.flex[i] = (cur[0], cur[1], sc)
                evaluate(net, shape, q)
                if q.score < best.score - 1e-4:
                    best, improved = q, True
        if not improved:
            break
    return best
