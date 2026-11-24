# Allofts

| Folder | What it is |
|---|---|
| `new-website/` | The redesigned website, ready to upload to a web host |
| `new-website-source/` | What generates it: text, photo choices and design |
| `previews/` | Screenshots of the new website on desktop and phone |
| `photos/` | The photos from the old site at full size, sorted by page and room |
| `website/` | A copy of the old allofts.gr site as downloaded |

## GPS-art route generator (`gps_art/`)

Turns text or a heart into a runnable route on London streets (OpenStreetMap walk network).

```
pip install osmnx networkx shapely geopandas gpxpy folium matplotlib numpy fonttools scikit-image osmium
# put an OSM extract at .cache/pbf/greater_london.osm.pbf (e.g. from download.openstreetmap.fr), or let it use Overpass
python -m gps_art.run --shapes heart,PHI_heart --areas Marylebone,Bloomsbury
```

Results go to `output/` (route GPX, preview PNG, interactive map, `summary.md`). That folder and the map cache are
gitignored, so routes stay on your machine.
