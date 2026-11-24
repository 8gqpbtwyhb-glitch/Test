"""Walkable street network: download (osmnx), clean, and fast routing helpers."""
from __future__ import annotations

import math
import os
import pickle
from dataclasses import dataclass

import networkx as nx
import numpy as np
import osmnx as ox
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
from shapely.geometry import LineString

CACHE = os.environ.get("GPS_ART_CACHE", os.path.join(os.path.dirname(__file__), "..", ".cache"))
UTM = "EPSG:32630"  # UTM zone 30N covers London; metres

# Hosts tried in order. overpass-api.de is the default; the kumi mirror is a fallback.
OVERPASS_URLS = ["https://overpass-api.de/api", "https://overpass.kumi.systems/api"]

ox.settings.use_cache = True
ox.settings.overpass_rate_limit = False   # the mirror's /status endpoint is non-standard
ox.settings.requests_timeout = 300
ox.settings.useful_tags_way = list(ox.settings.useful_tags_way) + [
    "access", "foot", "bridge", "tunnel", "service", "layer", "area", "covered", "indoor"]

# highway types we refuse to run on (on top of osmnx's own "walk" filter, which
# already drops motorways, access=private, foot=no and service=private)
BANNED_HIGHWAY = {"service", "corridor", "elevator", "escalator", "bus_stop", "platform",
                  "busway", "construction", "proposed", "raceway"}
BANNED_ACCESS = {"private", "no", "customers", "delivery", "agricultural", "forestry", "permit"}
MAJOR = {"trunk", "trunk_link", "primary", "primary_link", "secondary", "secondary_link"}


def _first(v):
    return v[0] if isinstance(v, list) else v


def download(name, lat, lon, dist):
    os.makedirs(CACHE, exist_ok=True)
    ox.settings.cache_folder = os.path.join(CACHE, "http")
    fn = os.path.join(CACHE, f"{name}_{dist}.pkl")
    if os.path.exists(fn):
        with open(fn, "rb") as f:
            return pickle.load(f)
    last = None
    for url in OVERPASS_URLS:
        ox.settings.overpass_url = url
        try:
            G = ox.graph_from_point((lat, lon), dist=dist, network_type="walk", simplify=True,
                                    retain_all=False)
            try:
                st = ox.features_from_point((lat, lon), dist=dist + 800,
                                            tags={"railway": ["station", "halt"]})
                st = st[st.geometry.notna()]
                stations = []
                for _, r in st.iterrows():
                    nm = r.get("name")
                    if not isinstance(nm, str):
                        continue
                    c = r.geometry.centroid
                    kind = []
                    for k in ("station", "network"):
                        v = r.get(k)
                        if isinstance(v, str):
                            kind.append(v)
                    stations.append((nm, c.y, c.x, "; ".join(kind)))
            except Exception as e:  # stations are a nicety, not essential
                print("station lookup failed:", e)
                stations = []
            with open(fn, "wb") as f:
                pickle.dump((G, stations), f)
            return G, stations
        except Exception as e:
            print(f"download via {url} failed: {e!r}")
            last = e
    raise last


@dataclass
class StreetNet:
    name: str
    G: nx.MultiGraph            # cleaned, undirected, projected (metres)
    xy: np.ndarray              # node coords (n,2)
    node_ids: list
    eu: np.ndarray              # edge endpoints (indices)
    ev: np.ndarray
    elen: np.ndarray            # edge length (m)
    ecost: np.ndarray           # base cost multiplier (steps etc.)
    egeom: list                 # LineString per edge, oriented u->v
    etags: list                 # dict per edge
    node_tree: cKDTree
    samp_xy: np.ndarray         # dense samples along every edge (for proximity)
    samp_ang: np.ndarray        # street bearing at sample (radians, mod pi)
    samp_edge: np.ndarray
    samp_tree: cKDTree
    stations: list              # (name, x, y, lat, lon, kind)
    crs: str = UTM

    # -------------------------------------------------------------------
    @classmethod
    def build(cls, name, G_raw, stations_ll):
        G = ox.project_graph(G_raw, to_crs=UTM)
        Gu = ox.convert.to_undirected(G)
        # drop banned ways
        drop = []
        for u, v, k, d in Gu.edges(keys=True, data=True):
            hw = _first(d.get("highway"))
            acc = _first(d.get("access"))
            foot = _first(d.get("foot"))
            if hw in BANNED_HIGHWAY or (acc in BANNED_ACCESS and foot not in ("yes", "designated", "permissive")):
                drop.append((u, v, k))
            elif _first(d.get("indoor")) in ("yes", "corridor") or _first(d.get("area")) == "yes":
                drop.append((u, v, k))
        Gu.remove_edges_from(drop)
        Gu.remove_edges_from(list(nx.selfloop_edges(Gu)))
        # largest connected component
        cc = max(nx.connected_components(Gu), key=len)
        Gu = Gu.subgraph(cc).copy()
        # prune dead ends repeatedly, so routes never run into a cul-de-sac and back
        while True:
            dead = [n for n in Gu if Gu.degree(n) <= 1]
            if not dead:
                break
            Gu.remove_nodes_from(dead)
        node_ids = list(Gu.nodes)
        idx = {n: i for i, n in enumerate(node_ids)}
        xy = np.array([[Gu.nodes[n]["x"], Gu.nodes[n]["y"]] for n in node_ids])
        eu, ev, elen, ecost, egeom, etags = [], [], [], [], [], []
        for u, v, k, d in Gu.edges(keys=True, data=True):
            geom = d.get("geometry")
            pu, pv = xy[idx[u]], xy[idx[v]]
            if geom is None:
                geom = LineString([pu, pv])
            else:
                c = np.asarray(geom.coords)
                if np.hypot(*(c[0] - pu)) > np.hypot(*(c[-1] - pu)):
                    geom = LineString(c[::-1])
            hw = _first(d.get("highway"))
            mult = 1.0
            if hw == "steps":
                mult = 2.5
            elif hw in ("trunk", "trunk_link"):
                mult = 1.3
            eu.append(idx[u]); ev.append(idx[v])
            elen.append(max(geom.length, 0.5)); ecost.append(mult)
            egeom.append(geom)
            etags.append({k2: d.get(k2) for k2 in ("highway", "name", "bridge", "tunnel", "oneway",
                                                   "access", "foot", "lanes", "osmid")})
        eu, ev = np.array(eu), np.array(ev)
        # dense samples for proximity / alignment scoring
        sx, sa, se = [], [], []
        for i, g in enumerate(egeom):
            L = g.length
            n = max(2, int(L // 8) + 1)
            pts = np.array([g.interpolate(t).coords[0] for t in np.linspace(0, L, n)])
            dd = np.diff(pts, axis=0)
            ang = np.arctan2(dd[:, 1], dd[:, 0])
            ang = np.r_[ang, ang[-1:]] % np.pi
            sx.append(pts); sa.append(ang); se.append(np.full(len(pts), i))
        samp_xy = np.vstack(sx)
        # stations in projected coords
        import pyproj
        tf = pyproj.Transformer.from_crs("EPSG:4326", UTM, always_xy=True)
        st = []
        seen = set()
        for nm, lat, lon, kind in stations_ll:
            if nm in seen:
                continue
            seen.add(nm)
            x, y = tf.transform(lon, lat)
            st.append((nm, x, y, lat, lon, kind))
        return cls(name, Gu, xy, node_ids, eu, ev, np.array(elen), np.array(ecost), egeom, etags,
                   cKDTree(xy), samp_xy, np.concatenate(sa), np.concatenate(se), cKDTree(samp_xy), st)

    # -------------------------------------------------------------------
    def nearest_station(self, p):
        if not self.stations:
            return None, float("inf")
        d = [math.hypot(p[0] - s[1], p[1] - s[2]) for s in self.stations]
        i = int(np.argmin(d))
        return self.stations[i], d[i]

    def proxy_cost(self, pts, tang, unit, k=6):
        """Cheap fit of a placed shape: per sample, distance to the nearest street
        plus a penalty when the street runs across the stroke. Returns mean / unit."""
        d, j = self.samp_tree.query(pts, k=k, distance_upper_bound=unit * 3)
        d = np.where(np.isinf(d), unit * 3, d)
        j = np.minimum(j, len(self.samp_ang) - 1)
        dang = np.abs(np.sin(self.samp_ang[j] - tang[:, None]))
        c = d + 0.35 * unit * dang
        return float(np.mean(np.min(c, axis=1)) / unit)

    # -------------------------------------------------------------------
    def route(self, waypts, unit, region_pad=400.0, alpha=6.0):
        """Route through a sequence of map-coordinate waypoints. Each leg is a
        shortest path where edges far from the leg's target segment cost more,
        so the route hugs the intended stroke. Returns (node index list, edge list)."""
        lo = waypts.min(axis=0) - region_pad
        hi = waypts.max(axis=0) + region_pad
        inbox = np.all((self.xy >= lo) & (self.xy <= hi), axis=1)
        emask = inbox[self.eu] & inbox[self.ev]
        E = np.nonzero(emask)[0]
        u, v = self.eu[E], self.ev[E]
        sub_nodes = np.nonzero(inbox)[0]
        remap = -np.ones(len(self.xy), int)
        remap[sub_nodes] = np.arange(len(sub_nodes))
        su, sv = remap[u], remap[v]
        n = len(sub_nodes)
        pu, pv = self.xy[u], self.xy[v]
        mid = (pu + pv) / 2
        base = self.elen[E] * self.ecost[E]
        sigma = 0.22 * unit

        # snap waypoints to nodes in the sub-network
        sub_tree = cKDTree(self.xy[sub_nodes])
        _, wn = sub_tree.query(waypts)
        # collapse repeats
        seq = [int(wn[0])]
        segs = []
        for i in range(1, len(wn)):
            if wn[i] != seq[-1]:
                seq.append(int(wn[i]))
                segs.append((waypts[i - 1], waypts[i]))
            else:
                if segs:
                    segs[-1] = (segs[-1][0], waypts[i])
        path_nodes = [seq[0]]
        for (a, b), s, t in zip(segs, seq[:-1], seq[1:]):
            ab = b - a
            L2 = max(ab @ ab, 1e-9)

            def segdist(P):
                tt = np.clip(((P - a) @ ab) / L2, 0, 1)
                Q = a + tt[:, None] * ab
                return np.hypot(*(P - Q).T)
            dev = (segdist(pu) + segdist(pv) + 2 * segdist(mid)) / 4
            w = base * (1 + alpha * (dev / sigma) ** 2)
            M = csr_matrix((np.r_[w, w], (np.r_[su, sv], np.r_[sv, su])), shape=(n, n))
            dist, pred = dijkstra(M, directed=True, indices=s, return_predecessors=True)
            if not np.isfinite(dist[t]):
                return None
            p = [t]
            while p[-1] != s:
                p.append(pred[p[-1]])
            path_nodes.extend(p[::-1][1:])
        full = [int(sub_nodes[i]) for i in path_nodes]
        return full

    def edge_lookup(self):
        if not hasattr(self, "_elk"):
            elk = {}
            for i, (a, b) in enumerate(zip(self.eu, self.ev)):
                for key in ((a, b), (b, a)):
                    if key not in elk or self.elen[i] < self.elen[elk[key]]:
                        elk[key] = i
            self._elk = elk
        return self._elk

    def path_geometry(self, nodes):
        """Full polyline (following street geometry) for a node path + edge ids."""
        elk = self.edge_lookup()
        coords = [self.xy[nodes[0]]]
        edges = []
        for a, b in zip(nodes[:-1], nodes[1:]):
            if a == b:
                continue
            e = elk[(a, b)]
            c = np.asarray(self.egeom[e].coords)
            if self.eu[e] != a:
                c = c[::-1]
            coords.extend(c[1:])
            edges.append(e)
        return np.array(coords), edges
