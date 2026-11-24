"""Build area street networks from a local OpenStreetMap extract (.osm.pbf)
instead of Overpass. Applies the same tag filter as osmnx's "walk" network."""
from __future__ import annotations

import math
import os
import pickle
import re

import osmium

# osmnx 2.x walk filter, as Python regexes ("!~" = must NOT match)
_NOT = {
    "area": "yes", "access": "private",
    "highway": "abandoned|bus_guideway|construction|cycleway|motor|no|planned|platform|proposed|raceway|razed|rest_area|services",
    "foot": "no", "service": "private",
    "sidewalk": "separate", "sidewalk:both": "separate", "sidewalk:left": "separate", "sidewalk:right": "separate",
}
_NOT = {k: re.compile(v) for k, v in _NOT.items()}
KEEP_TAGS = ("highway", "name", "access", "foot", "bridge", "tunnel", "oneway", "service", "layer",
             "area", "covered", "indoor", "lanes", "maxspeed", "junction", "width", "est_width", "ref")
BBOX = (51.42, -0.30, 51.60, 0.06)  # inner London (s, w, n, e)


def walk_ok(tags):
    if "highway" not in tags:
        return False
    for k, rx in _NOT.items():
        v = tags.get(k)
        if v is not None and rx.search(v):
            return False
    return True


class _H(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.ways, self.nodes, self.stations = [], {}, []

    def node(self, n):
        t = n.tags
        if t.get("railway") in ("station", "halt") and t.get("name"):
            loc = n.location
            if BBOX[0] - .02 < loc.lat < BBOX[2] + .02 and BBOX[1] - .03 < loc.lon < BBOX[3] + .03:
                self.stations.append((t.get("name"), loc.lat, loc.lon,
                                      "; ".join(v for v in (t.get("station"), t.get("network")) if v)))

    def way(self, w):
        tags = {t.k: t.v for t in w.tags}
        if not walk_ok(tags):
            return
        try:
            locs = [(nd.ref, nd.location.lat, nd.location.lon) for nd in w.nodes]
        except osmium.InvalidLocationError:
            return
        if not any(BBOX[0] < la < BBOX[2] and BBOX[1] < lo < BBOX[3] for _, la, lo in locs):
            return
        for ref, la, lo in locs:
            self.nodes[ref] = (la, lo)
        self.ways.append((w.id, [r for r, _, _ in locs], {k: tags[k] for k in KEEP_TAGS if k in tags}))


def extract(pbf, out):
    if os.path.exists(out):
        with open(out, "rb") as f:
            return pickle.load(f)
    h = _H()
    h.apply_file(pbf, locations=True)
    data = (h.ways, h.nodes, h.stations)
    with open(out, "wb") as f:
        pickle.dump(data, f)
    return data


def area_elements(data, lat, lon, dist):
    """Overpass-style JSON for ways touching the area's bounding box."""
    ways, nodes, stations = data
    dlat = dist / 111_320
    dlon = dist / (111_320 * math.cos(math.radians(lat)))
    s, n, w, e = lat - dlat, lat + dlat, lon - dlon, lon + dlon
    els, used = [], set()
    for wid, refs, tags in ways:
        if any(s < nodes[r][0] < n and w < nodes[r][1] < e for r in refs):
            els.append({"type": "way", "id": wid, "nodes": refs, "tags": tags})
            used.update(refs)
    for r in used:
        els.append({"type": "node", "id": r, "lat": nodes[r][0], "lon": nodes[r][1]})
    dl2, dn2 = dlat + 800 / 111_320, dlon + 800 / 111_320 / math.cos(math.radians(lat))
    st = [x for x in stations if abs(x[1] - lat) < dl2 and abs(x[2] - lon) < dn2]
    return {"elements": els}, st
