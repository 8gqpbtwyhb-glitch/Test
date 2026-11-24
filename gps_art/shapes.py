"""Turn text (and a heart) into ONE continuous runnable polyline.

Two ways to get letter strokes:
  * block letters: hand-designed centre-line strokes on a 4-unit-high grid
  * font letters: render a real font (matplotlib TextPath, so Greek works),
    skeletonize the glyphs to centre-lines and simplify them.

Either way every glyph becomes a small stroke graph. The strokes of one glyph
are put in order with a Chinese-postman tour (retracing the fewest stroke
lengths), glyphs are joined left to right with short connectors, and the
heart is appended as a closed loop.

All coordinates are in "units": letter height = 4 units, y up.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import networkx as nx
import numpy as np

# --------------------------------------------------------------------------
# block letters: list of polylines (each polyline is a list of (x, y))
# width noted per glyph so we can lay out text
# --------------------------------------------------------------------------
BLOCK = {
    "F": (2.0, [[(0, 0), (0, 4), (2, 4)], [(0, 2), (1.6, 2)]]),
    "O": (2.2, [[(0, 0), (0, 4), (2.2, 4), (2.2, 0), (0, 0)]]),
    "T": (2.4, [[(0, 4), (2.4, 4)], [(1.2, 4), (1.2, 0)]]),
    # serif I: the serifs keep it an "I" even when a connector touches it
    "I": (1.2, [[(0.6, 0), (0.6, 4)], [(0, 4), (1.2, 4)], [(0, 0), (1.2, 0)]]),
    "N": (2.2, [[(0, 0), (0, 4), (2.2, 0), (2.2, 4)]]),
    "|": (0.0, [[(0, 0), (0, 4)]]),        # plain I (no serifs)
    # Greek capital phi: a box-ish ring with a stem through it
    "Φ": (2.8, [[(0.3, 0.9), (0.3, 3.1), (2.5, 3.1), (2.5, 0.9), (0.3, 0.9)], [(1.4, 0), (1.4, 4)]]),
    "L": (2.0, [[(0, 4), (0, 0), (2, 0)]]),
    "V": (2.4, [[(0, 4), (1.2, 0), (2.4, 4)]]),
    "E": (2.0, [[(2, 4), (0, 4), (0, 0), (2, 0)], [(0, 2), (1.6, 2)]]),
}


def heart_curve(n: int = 64, height: float = 4.0):
    """Classic parametric heart, bottom tip at (0, 0), returned as closed loop
    starting and ending at the bottom tip."""
    t = np.linspace(math.pi, math.pi + 2 * math.pi, n + 1)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    y = y - y.min()
    s = height / (y.max() - y.min())
    pts = np.c_[x * s, y * s]
    pts[-1] = pts[0]
    return pts


# --------------------------------------------------------------------------
# font letters via skeletonization
# --------------------------------------------------------------------------
def font_glyph_strokes(text: str, font="DejaVu Sans", weight="bold", px_per_unit=40,
                       simplify_tol=0.12):
    """Return list of glyph stroke lists [(x0,width,[polyline,...]), ...] built
    from the real font outlines of `text`, scaled so capital height = 4 units.
    Returns None for any character the font lacks (renders as tofu)."""
    from matplotlib.font_manager import FontProperties, findfont
    from matplotlib.textpath import TextPath
    from matplotlib.path import Path
    from fontTools.ttLib import TTFont
    from skimage.morphology import skeletonize
    from shapely.geometry import LineString

    fp = FontProperties(family=font, weight=weight)
    ttf = TTFont(findfont(fp))
    cmap = ttf.getBestCmap()
    missing = [c for c in text if ord(c) not in cmap and not c.isspace()]
    if missing:
        raise ValueError(f"font {font!r} lacks glyphs for {missing}")

    cap = TextPath((0, 0), "H", size=100, prop=fp).get_extents().height
    scale = 4.0 / cap
    glyphs = []
    x_cursor = 0.0
    for ch in text:
        tp = TextPath((0, 0), ch, size=100, prop=fp)
        ext = tp.get_extents()
        adv = TextPath((0, 0), ch + "H", size=100, prop=fp).get_extents().width - \
            TextPath((0, 0), "H", size=100, prop=fp).get_extents().width
        verts = tp.vertices * scale
        # rasterize the glyph
        pad = 0.4
        x0, y0 = ext.x0 * scale - pad, ext.y0 * scale - pad
        x1, y1 = ext.x1 * scale + pad, ext.y1 * scale + pad
        W = int((x1 - x0) * px_per_unit)
        H = int((y1 - y0) * px_per_unit)
        xs = x0 + (np.arange(W) + 0.5) / px_per_unit
        ys = y0 + (np.arange(H) + 0.5) / px_per_unit
        XX, YY = np.meshgrid(xs, ys)
        path = Path(verts, tp.codes)
        # even-odd fill via the compound path's own polygons
        inside = np.zeros(XX.shape, bool)
        for poly in path.to_polygons():
            inside ^= Path(poly).contains_points(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)
        sk = skeletonize(inside)
        polylines = _skeleton_to_polylines(sk, xs, ys)
        strokes = []
        for pl in polylines:
            ls = LineString(pl).simplify(simplify_tol)
            if ls.length < 0.35:  # drop skeleton spurs
                continue
            strokes.append([(x, y) for x, y in ls.coords])
        glyphs.append((x_cursor, max(adv * scale, 0.5), strokes))
        x_cursor += adv * scale + 0.8
    return glyphs


def _skeleton_to_polylines(sk, xs, ys):
    """Trace a 1-px skeleton into polylines between junctions/endpoints."""
    pix = set(zip(*np.nonzero(sk)))
    nbr = lambda p: [(p[0] + dy, p[1] + dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                     if (dy or dx) and (p[0] + dy, p[1] + dx) in pix]
    G = nx.Graph()
    for p in pix:
        for q in nbr(p):
            G.add_edge(p, q)
    # remove 4-connected diagonal redundancy: keep graph simple via MST per comp
    T = nx.minimum_spanning_tree(G, weight=None)
    lines = []
    key = lambda p: p
    seen = set()
    nodes_special = {n for n in T if T.degree(n) != 2}
    for s in nodes_special:
        for nb in T.neighbors(s):
            e = frozenset((s, nb))
            if e in seen:
                continue
            path = [s, nb]
            seen.add(e)
            prev, cur = s, nb
            while cur not in nodes_special:
                nxt = [q for q in T.neighbors(cur) if q != prev][0]
                seen.add(frozenset((cur, nxt)))
                prev, cur = cur, nxt
                path.append(cur)
            lines.append([(xs[c], ys[r]) for r, c in path])
    # pure loops (no special node), e.g. "O"
    for comp in nx.connected_components(G):
        if not (comp & nodes_special):
            cyc = nx.cycle_basis(G.subgraph(comp))
            if cyc:
                c = max(cyc, key=len)
                lines.append([(xs[q[1]], ys[q[0]]) for q in c + [c[0]]])
    return lines


# --------------------------------------------------------------------------
# ordering strokes into one continuous line
# --------------------------------------------------------------------------
@dataclass
class Shape:
    name: str
    path: np.ndarray                     # (N,2) continuous polyline, units
    ink: list = field(default_factory=list)   # list of polylines that are "meant" to be seen
    connectors: list = field(default_factory=list)  # connector polylines
    letter_starts: list = field(default_factory=list)  # (label, (x,y))
    item: np.ndarray = None              # per path point: which glyph/part it belongs to

    @property
    def length(self):
        d = np.diff(self.path, axis=0)
        return float(np.hypot(d[:, 0], d[:, 1]).sum())


def _glyph_graph(strokes, nd=4):
    from shapely.geometry import MultiLineString
    from shapely.ops import unary_union
    G = nx.Graph()
    r = lambda p: (round(p[0], nd), round(p[1], nd))
    # node the strokes so T-junctions (e.g. F's middle arm) become vertices
    merged = unary_union(MultiLineString([pl for pl in strokes if len(pl) > 1]))
    parts = getattr(merged, "geoms", [merged])
    for ls in parts:
        pl = list(ls.coords)
        # subdivide so connectors may attach part-way along a stroke
        dense = [pl[0]]
        for a, b in zip(pl[:-1], pl[1:]):
            n = max(1, int(math.ceil(math.dist(a, b) / 0.5)))
            dense += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(1, n + 1)]
        pl = dense
        for a, b in zip(pl[:-1], pl[1:]):
            a, b = r(a), r(b)
            if a != b:
                G.add_edge(a, b, weight=math.dist(a, b))
    # merge nodes that almost coincide (skeleton noise)
    return G


def _postman_path(G, start, end):
    """Shortest walk from start to end covering every edge of G."""
    odd = {n for n in G if G.degree(n) % 2}
    for n in (start, end):
        if start != end:
            odd ^= {n}
    M = nx.MultiGraph(G)
    odd = list(odd)
    if odd:
        dist = dict(nx.all_pairs_dijkstra_path_length(G))
        K = nx.Graph()
        for i, a in enumerate(odd):
            for b in odd[i + 1:]:
                K.add_edge(a, b, weight=-dist[a][b])
        match = nx.max_weight_matching(K, maxcardinality=True)
        for a, b in match:
            p = nx.dijkstra_path(G, a, b)
            for u, v in zip(p[:-1], p[1:]):
                M.add_edge(u, v, weight=G[u][v]["weight"])
    if start == end:
        circ = list(nx.eulerian_circuit(M, source=start))
    else:
        circ = list(nx.eulerian_path(M, source=start))
    pts = [circ[0][0]] + [v for _, v in circ]
    return pts


def _choose_link(Ga, Gb, level=None):
    """Closest pair of nodes (a in Ga, b in Gb); `level` in units biases the
    connector height (e.g. 4 = top line, 0 = baseline)."""
    best = None
    for a in Ga:
        for b in Gb:
            d = math.dist(a, b)
            if level is not None:
                d += 2.0 * (abs(a[1] - level) + abs(b[1] - level))
            d += 0.5 * abs(a[1] - b[1])  # prefer horizontal connectors
            if best is None or d < best[0]:
                best = (d, a, b)
    return best[1], best[2]


def build_shape(name, glyphs, links=None, heart=True, heart_height=4.4, heart_gap=1.2,
                start_hint=None):
    """glyphs: list of (x_offset, width, strokes). links: list of preferred
    connector heights (None = auto) between consecutive items (heart counts)."""
    Gs = []
    for x0, w, strokes in glyphs:
        G = _glyph_graph([[(x + x0, y) for x, y in pl] for pl in strokes])
        # detached parts (accents, dots) become their own items, left to right
        comps = sorted((G.subgraph(c).copy() for c in nx.connected_components(G)),
                       key=lambda g: (min(n[0] for n in g), -max(n[1] for n in g)))
        Gs.extend(comps)
    xmax = max(max(n[0] for n in G) for G in Gs) if Gs else 0.0
    heart_pts = None
    if heart:
        hp = heart_curve(height=heart_height)
        hw = hp[:, 0].max() - hp[:, 0].min()
        hp[:, 0] += xmax + heart_gap + hw / 2 if Gs else 0
        heart_pts = hp
        Gs.append(_heart_graph(hp))
    labels = list(name) + (["heart"] if heart else [])
    return _assemble(name, Gs, labels, links, start_hint)


def _heart_graph(hp):
    Gh = nx.Graph()
    for a, b in zip(hp[:-1], hp[1:]):
        a, b = (round(a[0], 4), round(a[1], 4)), (round(b[0], 4), round(b[1], 4))
        Gh.add_edge(a, b, weight=math.dist(a, b))
    return Gh


def build_layout(name, parts, links=None, start_hint=None):
    """Free 2-D layout, items given in DRAWING order (not reading order):
    ("glyph", ch, x0, y0, xscale) or ("heart", centre_x, bottom_y, height).
    links[i] = preferred connector height (absolute units) between item i and i+1."""
    Gs, labels = [], []
    for part in parts:
        if part[0] == "heart":
            _, cx, by, h = part
            hp = heart_curve(n=72, height=h)
            hp[:, 0] += cx
            hp[:, 1] += by
            Gs.append(_heart_graph(hp)); labels.append("heart")
        else:
            _, ch, x0, y0, xs = part
            w, strokes = BLOCK[ch]
            xs = 1.0 if ch in "I|" else xs
            Gs.append(_glyph_graph([[(px * xs + x0, py + y0) for px, py in pl] for pl in strokes]))
            labels.append("I" if ch == "|" else ch)
    return _assemble(name, Gs, labels, links, start_hint)


def _assemble(name, Gs, labels, links, start_hint=None):
    links = list(links) if links and len(links) == len(Gs) - 1 else [None] * (len(Gs) - 1)

    # decide entry/exit node of each item
    entries, exits = [None] * len(Gs), [None] * len(Gs)
    for i in range(len(Gs) - 1):
        a, b = _choose_link(Gs[i], Gs[i + 1], links[i])
        exits[i], entries[i + 1] = a, b
    if entries[0] is None:
        # start: an end-point (odd node) of the first glyph, lowest-left preferred
        odd = [n for n in Gs[0] if Gs[0].degree(n) % 2] or list(Gs[0])
        cand = [n for n in odd if n != exits[0]] or odd
        entries[0] = start_hint if start_hint in Gs[0] else min(cand, key=lambda n: (n[0] + n[1] * 0.3))
        if len(Gs) == 1:
            # single closed item -> loop
            exits[0] = entries[0]
    if exits[-1] is None:
        odd = [n for n in Gs[-1] if Gs[-1].degree(n) % 2 and n != entries[-1]]
        exits[-1] = max(odd, key=lambda n: n[0]) if odd else entries[-1]

    path, ink, conns, starts, item = [], [], [], [], []
    for i, G in enumerate(Gs):
        seg = _postman_path(G, entries[i], exits[i])
        starts.append((labels[i] if i < len(labels) else f"#{i}", seg[0]))
        if path:
            conns.append([path[-1], seg[0]])
        path.extend(seg)
        item.extend([i] * len(seg))
        for u, v in G.edges():
            ink.append([u, v])
    return Shape(name=name, path=np.array(path, float), ink=ink, connectors=conns,
                 letter_starts=starts, item=np.array(item))


def block_word(word, spacing=None, xscale=1.0, name=None, **kw):
    spacing = spacing or {}
    glyphs, x = [], 0.0
    for i, ch in enumerate(word):
        w, strokes = BLOCK[ch]
        if ch not in "I|":   # keep I narrow
            w, strokes = w * xscale, [[(px * xscale, py) for px, py in pl] for pl in strokes]
        glyphs.append((x, w, strokes))
        x += w + spacing.get(i, 1.0)
    sh = build_shape(word.replace("|", "I"), glyphs, **kw)
    sh.name = name or word
    return sh


def heart_only(height=4.0):
    hp = heart_curve(n=72, height=height)
    return Shape(name="heart", path=hp, ink=[[tuple(a), tuple(b)] for a, b in zip(hp[:-1], hp[1:])],
                 letter_starts=[("heart", tuple(hp[0]))], item=np.zeros(len(hp), int))


def font_word(text, name=None, heart=True, **kw):
    glyphs = font_glyph_strokes(text, **kw)
    glyphs = [g for g in glyphs if g[2]]
    return build_shape(name or text, glyphs, heart=heart)


# --------------------------------------------------------------------------
def flexed(shape: Shape, offsets):
    """Copy of `shape` with item i moved by offsets[i] = (dx, dy, scale) in units
    (scale about the item's own centre). Connectors stretch to follow."""
    if not offsets:
        return shape
    P = shape.path.copy()
    for i, t in offsets.items():
        m = shape.item == i
        if not m.any():
            continue
        lo, hi = shape.path[m].min(axis=0), shape.path[m].max(axis=0)
        if len(t) in (4, 5):   # move box edges: (left, right, bottom, top[, rot deg]), units
            dl, dr, db, dt = t[:4]
            span = np.maximum(hi - lo, 1e-9)
            f = (shape.path[m] - lo) / span
            nlo = lo + np.array([dl, db])
            nhi = hi + np.array([dr, dt])
            flat = (hi - lo) < 1e-6
            Q = nlo + f * (nhi - nlo)
            Q[:, flat] = shape.path[m][:, flat] + np.array([dl, db])[flat]
            if len(t) == 5 and t[4]:
                a = math.radians(t[4])
                c = (nlo + nhi) / 2
                R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
                Q = (Q - c) @ R.T + c
            P[m] = Q
        else:
            dx, dy, sc = t
            c = (lo + hi) / 2
            P[m] = (shape.path[m] - c) * sc + c + np.array([dx, dy])
    return Shape(shape.name, P, shape.ink, shape.connectors, shape.letter_starts, shape.item)


def densify(path, step):
    """Resample a polyline every `step` units (keeps vertices)."""
    out = [path[0]]
    for a, b in zip(path[:-1], path[1:]):
        d = np.hypot(*(b - a))
        n = max(1, int(math.ceil(d / step)))
        for k in range(1, n + 1):
            out.append(a + (b - a) * k / n)
    return np.array(out)


def candidate_shapes():
    """Named shape variants the search tries."""
    S = {}
    # FOTINI: F->O and O->T joined along the top line, T->I->N->I along the
    # baseline (serifed I keeps them readable), then the heart.
    S["FOTINI"] = block_word("FOTINI", links=[2, 4, 0, 0, 4, 0], spacing=dict.fromkeys(range(6), 1.4))
    S["FOTINI_wide"] = block_word("FOTINI", links=[2, 4, 0, 0, 4, 0], xscale=1.35, name="FOTINI_wide",
                                  spacing=dict.fromkeys(range(6), 1.4))
    # roomier layout: wider gaps keep connectors from fusing letters; bigger heart
    S["FOTINI_v2"] = block_word("FOTINI", links=[2, 4, 0, 0, 4, 0], xscale=1.15, name="FOTINI_v2",
                                spacing=dict.fromkeys(range(6), 2.0), heart_height=5.6, heart_gap=1.8)
    # underline style: plain I's, letters joined along the baseline from O onwards
    S["FOTINI_ul"] = block_word("FOT|N|", links=[2, 0, 0, 0, 0, 0], xscale=1.15, name="FOTINI_ul",
                                spacing={0: 1.3, 1: 1.3, 2: 1.4, 3: 1.4, 4: 1.4, 5: 1.6}, heart_height=5.0)
    # two rows: FOTI / NI + heart. Drawn F,O,T,I then down to the heart, then I, N
    # right-to-left so that every connector is short.
    R2 = -5.8
    S["FOTINI_2row"] = build_layout("FOTINI_2row", [
        ("glyph", "F", 0.0, 0, 1.15), ("glyph", "O", 3.6, 0, 1.15), ("glyph", "T", 7.3, 0, 1.15),
        ("glyph", "I", 11.4, 0, 1.0),
        ("heart", 9.4, R2, 4.6), ("glyph", "I", 5.0, R2, 1.0), ("glyph", "N", 1.0, R2, 1.15)],
        links=[2, 4, 0, -0.6, R2, R2])
    # LO / VE + heart: V first, up into L, then O, down into E, then the heart
    S["LOVE_2row"] = build_layout("LOVE_2row", [
        ("glyph", "V", 0.2, R2, 1.15), ("glyph", "L", 0.0, 0, 1.2), ("glyph", "O", 3.6, 0, 1.3),
        ("glyph", "E", 4.2, R2, 1.2), ("heart", 10.6, R2, 4.6)],
        links=[R2 + 4, 0, -0.9, R2])
    # one big initial + heart (letters ~1 km tall fit in 12 km)
    S["F_heart"] = build_layout("F_heart", [("glyph", "F", 0, 0, 1.2), ("heart", 6.0, 0, 4.4)], links=[2.2])
    S["PHI_heart"] = build_layout("PHI_heart", [("glyph", "Φ", 0, 0, 1.0), ("heart", 6.2, 0, 4.4)], links=[2.2])
    S["LOVE"] = block_word("LOVE", links=[0, 0, 4, 0], spacing=dict.fromkeys(range(4), 1.3))
    S["heart"] = heart_only()
    return S
