# Allofts website: source

This folder builds the finished website in `../new-website`.

| File | What it holds |
|---|---|
| `content.py` | Every word (English and Greek), prices, phone numbers, links, and which photos appear where |
| `build.py` | Turns the content and the photos into the finished pages |
| `static/css/site.css` | The design |
| `static/js/site.js` | The interactions (menu, slideshow, photo viewer, enquiry form) |
| `static/fonts`, `static/img` | Fonts and logo files |

## Changing something

1. Edit `content.py` (for example the `price_from` number, a description, or a room's photo list).
2. Run `python3 build.py`. It needs Python 3 with Pillow (`pip install pillow`).
3. Upload the contents of `../new-website` to the web host.

Photos are read from `../photos`. Each room only uses photos from its own folder there.
Run `python3 build.py --clean` to rebuild everything from scratch.

## Looking at the site on your computer

```
cd ../new-website
python3 -m http.server 8000
```

Then open http://localhost:8000 in a browser.
