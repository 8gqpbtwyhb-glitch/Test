#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the Allofts website into ../new-website.

    python3 build.py            build the site (photos are only re-made when they change)
    python3 build.py --clean    delete the output folder first and rebuild everything

Words, prices and photo choices live in content.py; the look lives in static/css/site.css.
"""
import os, sys, json, html, shutil, hashlib, datetime
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageOps
import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.normpath(os.path.join(HERE, "..", "photos"))
OUT = os.path.normpath(os.path.join(HERE, "..", "new-website"))
CACHE_FILE = os.path.join(HERE, ".image-cache.json")
YEAR = datetime.date.today().year
WIDTHS = [480, 800, 1200, 1800]
LEAD_WIDTHS = WIDTHS + [2400]
ROOM = {r["slug"]: r for r in C.ROOMS}
BLANK = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="

# ---------------------------------------------------------------- images ----
IMAGES, MAN = {}, {}

def register_images():
    for r in C.ROOMS:
        for i, (fn, tag) in enumerate(r["photos"], 1):
            IMAGES[f"{r['slug']}-{i:02d}"] = dict(src=f"rooms/{r['slug']}/{fn}", tag=tag, base=f"img/{r['slug']}/{i:02d}",
                                                   room=r["slug"], widths=LEAD_WIDTHS if i == 1 else WIDTHS, crop=None)
    for hid, (fn, tag) in C.HOUSE.items():
        IMAGES[hid] = dict(src=fn, tag=tag, base=f"img/house/{hid}", room=None,
                           widths=LEAD_WIDTHS if hid in ("ext-day", "ext-night", "ext-entrance") else WIDTHS, crop=None)
    for k, (slug, n, wide, tall) in enumerate(C.HERO):
        src = IMAGES[f"{slug}-{n:02d}"]["src"]
        IMAGES[f"hero-{k}-wide"] = dict(src=src, tag="view", base=f"img/hero/{k + 1}-wide", room=slug, widths=[1280, 1920, 2560], crop=(16 / 9, *wide))
        IMAGES[f"hero-{k}-tall"] = dict(src=src, tag="view", base=f"img/hero/{k + 1}-tall", room=slug, widths=[540, 810, 1080], crop=(9 / 16, *tall))

def _open(src):
    im = ImageOps.exif_transpose(Image.open(src))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")

def _crop(im, crop):
    ar, fx, fy = crop
    W, H = im.size
    if W / H > ar: nw, nh = round(H * ar), H
    else: nw, nh = W, round(W / ar)
    x, y = round((W - nw) * fx), round((H - nh) * fy)
    return im.crop((x, y, x + nw, y + nh))

def make_variants(job):
    """Runs in a worker process: writes the WebP sizes for one photo."""
    src, out_base, widths, crop = job
    im = _open(src)
    if crop: im = _crop(im, crop)
    W, H = im.size
    ws = [w for w in widths if w <= W]
    if W < widths[-1] and (not ws or W > ws[-1] * 1.12): ws.append(W)
    os.makedirs(os.path.dirname(out_base), exist_ok=True)
    variants = []
    for w in ws:
        h = round(H * w / W)
        r = im if w == W else im.resize((w, h), Image.LANCZOS)
        r.save(f"{out_base}-{w}.webp", "WEBP", quality=80 if w <= 1200 else 78, method=6)
        variants.append([w, h])
    r, g, b = im.resize((1, 1), Image.BOX).getpixel((0, 0))
    return dict(w=W, h=H, variants=variants, color="#%02x%02x%02x" % (r, g, b))

def build_images():
    cache = json.load(open(CACHE_FILE)) if os.path.exists(CACHE_FILE) else {}
    jobs, keys = [], {}
    for iid, m in IMAGES.items():
        src = os.path.join(PHOTOS, m["src"])
        st = os.stat(src)
        key = hashlib.md5(json.dumps([m["src"], st.st_size, int(st.st_mtime), m["widths"], m["crop"], m["base"], 3]).encode()).hexdigest()
        keys[iid] = key
        hit = cache.get(iid)
        out_base = os.path.join(OUT, "assets", m["base"])
        if hit and hit["key"] == key and all(os.path.exists(f"{out_base}-{w}.webp") for w, _ in hit["variants"]):
            MAN[iid] = hit
        else:
            jobs.append((iid, (src, out_base, m["widths"], m["crop"])))
    if jobs:
        print(f"  making {len(jobs)} photos…", flush=True)
        with ProcessPoolExecutor() as ex:
            for (iid, _), res in zip(jobs, ex.map(make_variants, [j for _, j in jobs], chunksize=2)):
                res["key"] = keys[iid]
                MAN[iid] = res
    for iid in MAN: MAN[iid]["base"] = IMAGES[iid]["base"]
    json.dump({k: MAN[k] for k in IMAGES}, open(CACHE_FILE, "w"))
    # social-share picture
    og = os.path.join(OUT, "assets", "img", "og.jpg")
    if not os.path.exists(og):
        slug, n, wide, _ = C.HERO[0]
        im = _crop(_open(os.path.join(PHOTOS, IMAGES[f"{slug}-{n:02d}"]["src"])), (1200 / 630, wide[0], wide[1]))
        im.resize((1200, 630), Image.LANCZOS).save(og, "JPEG", quality=84, optimize=True, progressive=True)

# ------------------------------------------------------------- helpers ----
def esc(s): return html.escape(str(s), quote=True)

ICON = {
    "arrow": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>',
    "back":  '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12H5M11 6l-6 6 6 6"/></svg>',
    "out":   '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>',
    "down":  '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v15M6 13l6 6 6-6"/></svg>',
}

class Ctx:
    """Where we are: language and page path. Makes links that work from any folder depth."""
    def __init__(self, lang, path, absolute=False):
        self.lang, self.path, self.t = lang, path, C.T[lang]
        self.prefix = "" if lang == "en" else "el/"
        self.root = "/" if absolute else "../" * (self.prefix + path).count("/")
    def url(self, path=""):
        return (self.root + self.prefix + path) or "./"
    def other(self):
        return (self.root + ("el/" if self.lang == "en" else "") + self.path) or "./"
    def asset(self, p): return self.root + "assets/" + p
    def abs(self, lang=None, path=None):
        lang = lang or self.lang
        return C.SITE["url"] + "/" + ("" if lang == "en" else "el/") + (self.path if path is None else path)
    @property
    def booking(self): return C.SITE["booking"][self.lang]

def label(ctx, iid):
    m = IMAGES[iid]
    tag = ctx.t["tags"][m["tag"]]
    return f"{ROOM[m['room']]['name']} — {tag}" if m["room"] else f"Allofts — {tag}"

def srcset(ctx, iid):
    m = MAN[iid]
    return ", ".join(f"{ctx.asset(m['base'])}-{w}.webp {w}w" for w, _ in m["variants"])

def src_near(ctx, iid, target=800):
    m = MAN[iid]
    w = min((v[0] for v in m["variants"]), key=lambda x: abs(x - target))
    return f"{ctx.asset(m['base'])}-{w}.webp"

def img(ctx, iid, sizes, cls="", lazy=True, alt=None, attrs=""):
    m = MAN[iid]
    alt = label(ctx, iid) if alt is None else alt
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{src_near(ctx, iid)}" srcset="{srcset(ctx, iid)}" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" '
            f'alt="{esc(alt)}" {load} style="background-color:{m["color"]}"{attrs}>')

def frame(ctx, iid, sizes, ratio="", cls="", reveal=True, lazy=True, attrs=""):
    r = f" frame--{ratio}" if ratio else ""
    rv = ' data-reveal="img"' if reveal else ""
    return f'<figure class="frame{r} {cls}"{rv}{attrs}>{img(ctx, iid, sizes, lazy=lazy)}</figure>'

def lb(ctx, iid, inner, group, cls="", attrs=""):
    m = MAN[iid]
    w, h = m["variants"][-1]
    return (f'<a class="lb {cls}" href="{ctx.asset(m["base"])}-{w}.webp" data-lb="{group}" data-srcset="{srcset(ctx, iid)}" '
            f'data-w="{w}" data-h="{h}" data-caption="{esc(label(ctx, iid))}"{attrs}>{inner}</a>')

SZ_FULL = "100vw"
SZ_HALF = "(min-width: 900px) 50vw, 100vw"
SZ_THIRD = "(min-width: 1000px) 33vw, (min-width: 600px) 50vw, 100vw"
SZ_MASONRY = "(min-width: 1000px) 33vw, 50vw"
SZ_QUARTER = "(min-width: 900px) 25vw, 50vw"
SZ_CARD = "(min-width: 1200px) 28vw, (min-width: 700px) 42vw, 80vw"

def room_no(r): return f"{C.ROOMS.index(r) + 1:02d}"
def room_id(r, n=1): return f"{r['slug']}-{n:02d}"
def price(ctx, r): return ctx.t["price_from"].format(p=r.get("price", C.SITE["price_from"]))
def size(ctx, r): return f"{r['size']} {ctx.t['sqm']}"
def specs(ctx, r):
    t = ctx.t
    out = [size(ctx, r), t["upto"].format(n=r["guests"]), t["bed_queen"]]
    if r["sofa"]: out.append(t[f"sofa_{r['sofa']}"])
    if r["extra"]: out.append(C.EXTRA[r["extra"]][ctx.lang])
    return out

def tel_links(sep=" "):
    return sep.join(f'<a href="tel:{d}">{s}</a>' for d, s in C.SITE["phones"])

# ------------------------------------------------------------ page shell ----
def head(ctx, title, desc, og=None, preload=""):
    t = ctx.t
    other = "el" if ctx.lang == "en" else "en"
    full = title if "Allofts" in title else f"{title} — Allofts"
    fonts = ["noto-serif-display-latin-wght-normal", "manrope-latin-wght-normal"]
    if ctx.lang == "el": fonts += ["noto-serif-display-greek-wght-normal", "manrope-greek-wght-normal"]
    pre = "".join(f'<link rel="preload" href="{ctx.asset("fonts/" + f + ".woff2")}" as="font" type="font/woff2" crossorigin>\n' for f in fonts)
    og = og or (C.SITE["url"] + "/assets/img/og.jpg")
    return f'''<!doctype html>
<html lang="{ctx.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{ctx.abs()}">
<link rel="alternate" hreflang="{ctx.lang}" href="{ctx.abs()}">
<link rel="alternate" hreflang="{other}" href="{ctx.abs(other)}">
<link rel="alternate" hreflang="x-default" href="{ctx.abs('en')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Allofts">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{ctx.abs()}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="{'en_GB' if ctx.lang == 'en' else 'el_GR'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#131417">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="{ctx.asset('img/favicon.ico')}" sizes="48x48">
<link rel="icon" href="{ctx.asset('img/favicon-32.png')}" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{ctx.asset('img/apple-touch-icon.png')}">
<link rel="manifest" href="{ctx.root}site.webmanifest">
{pre}{preload}<link rel="stylesheet" href="{ctx.asset('css/site.css')}">
<script type="speculationrules">{{"prerender":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"selector_matches":"[target=_blank]"}}}}]}},"eagerness":"moderate"}}]}}</script>
<script>document.documentElement.className+=" js";setTimeout(function(){{if(!window.__allofts)document.documentElement.classList.remove("js")}},4000)</script>
</head>
'''

def header(ctx, current=""):
    t = ctx.t
    def link(path, key):
        cur = ' aria-current="page"' if current == path else ""
        return f'<a href="{ctx.url(path)}"{cur}>{esc(t[key])}</a>'
    nav = [("rooms/", "nav_rooms"), ("about/", "nav_house"), ("gallery/", "nav_gallery"), ("contact/", "nav_contact")]
    other = "el" if ctx.lang == "en" else "en"
    menu_links = "".join(f'<a href="{ctx.url(p)}"{" aria-current=page" if current == p else ""}><span>{i:02d}</span>{esc(t[k])}</a>'
                         for i, (p, k) in enumerate([("", "nav_home")] + nav, 1))
    return f'''<a class="skip" href="#main">{esc(t["skip"])}</a>
<header class="site-header" data-header>
  <a class="brand" href="{ctx.url()}" aria-label="Allofts — {esc(t["nav_home"])}">
    <img src="{ctx.asset("img/mark.png")}" width="59" height="40" alt="">
    <span class="brand__word">Allofts</span>
  </a>
  <nav class="site-nav" aria-label="{esc(t["menu"])}">{"".join(link(p, k) for p, k in nav)}</nav>
  <div class="site-header__side">
    <a class="lang" href="{ctx.other()}" lang="{other}" hreflang="{other}" title="{esc(t["other_name"])}">{t["other_short"]}</a>
    <a class="btn btn--gold btn--sm" href="{ctx.booking}" target="_blank" rel="noopener">{esc(t["book"])}</a>
    <button class="burger" type="button" aria-controls="menu" aria-expanded="false" aria-label="{esc(t["menu"])}" data-burger><i></i><i></i></button>
  </div>
</header>
<div class="menu" id="menu" data-menu aria-hidden="true">
  <nav class="menu__nav" aria-label="{esc(t["menu"])}">{menu_links}</nav>
  <div class="menu__foot">
    <a class="btn btn--gold" href="{ctx.booking}" target="_blank" rel="noopener">{esc(t["book"])} {ICON["out"]}</a>
    <p class="menu__contact">{tel_links("<br>")}<br><a href="mailto:{C.SITE["email"]}">{C.SITE["email"]}</a></p>
    <a class="menu__lang" href="{ctx.other()}" lang="{other}" hreflang="{other}">{esc(t["other_name"])}</a>
  </div>
</div>
'''

def footer(ctx):
    t = ctx.t
    other = "el" if ctx.lang == "en" else "en"
    addr = "<br>".join(esc(a) for a in C.SITE["address"][ctx.lang])
    nav = [("rooms/", "nav_rooms"), ("about/", "nav_house"), ("gallery/", "nav_gallery"), ("contact/", "nav_contact")]
    return f'''<footer class="site-footer theme-dark">
  <div class="wrap site-footer__top">
    <div class="site-footer__brand">
      <img src="{ctx.asset("img/logo-full.png")}" width="168" height="171" alt="Allofts — Contemporary Living" loading="lazy">
      <p>{esc(t["motto"])}</p>
    </div>
    <div>
      <h2 class="site-footer__h">{esc(t["f_visit"])}</h2>
      <address>{addr}</address>
      <p><a class="ul" href="{C.SITE["maps_link"]}" target="_blank" rel="noopener">{esc(t["loc_maps"])}</a></p>
    </div>
    <div>
      <h2 class="site-footer__h">{esc(t["f_call"])}</h2>
      <p>{tel_links("<br>")}</p>
      <p><a class="ul" href="mailto:{C.SITE["email"]}">{C.SITE["email"]}</a></p>
    </div>
    <div>
      <h2 class="site-footer__h">{esc(t["f_explore"])}</h2>
      <ul>{"".join(f'<li><a href="{ctx.url(p)}">{esc(t[k])}</a></li>' for p, k in nav)}</ul>
    </div>
    <div>
      <h2 class="site-footer__h">{esc(t["f_follow"])}</h2>
      <ul>
        <li><a href="{C.SITE["instagram"]}" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="{C.SITE["facebook"]}" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="{ctx.booking}" target="_blank" rel="noopener">Booking.com</a></li>
      </ul>
    </div>
  </div>
  <div class="site-footer__word" aria-hidden="true">Allofts</div>
  <div class="wrap site-footer__bottom">
    <p>© {YEAR} Allofts. {esc(t["f_rights"])}</p>
    <p><a href="{ctx.url("privacy-policy/")}">{esc(t["f_privacy"])}</a><span aria-hidden="true">·</span><a href="{ctx.other()}" lang="{other}" hreflang="{other}">{esc(t["other_name"])}</a><span aria-hidden="true">·</span><a href="#main">{esc(t["f_top"])}</a></p>
  </div>
</footer>
<div class="dock" data-dock>
  <a href="tel:{C.SITE["phones"][1][0]}">{esc(t["call"])}</a>
  <a class="dock__book" href="{ctx.booking}" target="_blank" rel="noopener">{esc(t["book"])}</a>
</div>
'''

def page(ctx, title, desc, body, body_class="top-light", current="", og=None, preload="", jsonld=None):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n' if jsonld else ""
    return (head(ctx, title, desc, og, preload) + f'<body class="{body_class}">\n' + header(ctx, current)
            + f'<main id="main">\n{body}\n</main>\n' + footer(ctx) + ld
            + f'<script src="{ctx.asset("js/site.js")}" defer></script>\n</body>\n</html>\n')

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(content)

# ------------------------------------------------------ shared sections ----
def card(ctx, r):
    t = ctx.t
    return f'''<article class="card">
  <a class="card__link" href="{ctx.url("rooms/" + r["slug"] + "/")}">
    <figure class="frame frame--45 card__media">{img(ctx, room_id(r), SZ_CARD)}<span class="card__badge" aria-hidden="true">{esc(t["view"])}</span></figure>
    <p class="card__row"><span class="num">{room_no(r)}</span><span>{esc(t["kind"][r["kind"]])} · {size(ctx, r)}</span></p>
    <h3 class="card__name">{esc(r["name"])}</h3>
    <p class="card__meta">{esc(t["upto"].format(n=r["guests"]))} · {esc(price(ctx, r))} {esc(t["per_night"])}</p>
  </a>
</article>'''

def rail(ctx, rooms, label_):
    t = ctx.t
    return f'''<div class="rail" data-rail tabindex="0" role="region" aria-label="{esc(label_)}">
{"".join(card(ctx, r) for r in rooms)}
</div>'''

def rail_nav(ctx):
    t = ctx.t
    return (f'<div class="rail-nav"><button type="button" data-rail-prev aria-label="{esc(t["prev"])}">{ICON["back"]}</button>'
            f'<button type="button" data-rail-next aria-label="{esc(t["next"])}">{ICON["arrow"]}</button></div>')

def amenities(ctx, keys, eyebrow=True):
    t = ctx.t
    items = "".join(f'<li><span class="num">{i:02d}</span>{esc(C.FACILITIES[k][ctx.lang])}</li>' for i, k in enumerate(keys, 1))
    return f'''<section class="amen sec theme-sand">
  <div class="wrap amen__grid">
    <div class="amen__head" data-reveal>
      <p class="eyebrow">{esc(t["amen_eyebrow"])}</p>
      <h2 class="h2">{esc(t["amen_title"])}</h2>
      <p>{esc(t["amen_p"])}</p>
    </div>
    <ul class="amen__list" data-reveal>{items}</ul>
  </div>
</section>'''

def location(ctx):
    t = ctx.t
    addr = "<br>".join(esc(a) for a in C.SITE["address"][ctx.lang])
    return f'''<section class="loc sec theme-dark" id="location">
  <div class="wrap loc__grid">
    <div class="loc__text" data-reveal>
      <p class="eyebrow">{esc(t["loc_eyebrow"])}</p>
      <h2 class="h2">{esc(t["loc_title"])}</h2>
      <p>{esc(t["loc_p"])}</p>
      <address>{addr}</address>
      <div class="btn-row">
        <a class="btn btn--light" href="{C.SITE["maps_link"]}" target="_blank" rel="noopener">{esc(t["loc_maps"])} {ICON["out"]}</a>
      </div>
    </div>
    {frame(ctx, "aerial", SZ_HALF, "169", "loc__img")}
  </div>
  <div class="wrap">
    <div class="map" data-map data-src="{esc(C.SITE["maps_embed"])}" data-title="{esc(t["loc_title"])}">
      <div class="map__inner">
        <p class="map__addr">{esc(t["loc_title"])}</p>
        <button class="btn btn--ghost-light" type="button" data-map-load>{esc(t["loc_load"])}</button>
        <p class="map__note">{esc(t["loc_note"])}</p>
      </div>
    </div>
  </div>
</section>'''

def cta(ctx):
    t = ctx.t
    return f'''<section class="cta theme-dark">
  <div class="cta__bg" data-parallax>{img(ctx, "ext-night", SZ_FULL, alt="")}</div>
  <div class="wrap cta__inner" data-reveal>
    <p class="eyebrow">{esc(t["tagline"])}</p>
    <h2 class="h1">{esc(t["cta_title"])}</h2>
    <p class="cta__p">{esc(t["cta_p"])}</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--gold" href="{ctx.booking}" target="_blank" rel="noopener">{esc(t["book"])} {ICON["out"]}</a>
      <a class="btn btn--ghost-light" href="{ctx.url("contact/")}">{esc(t["enquire"])}</a>
    </div>
    <p class="cta__phones">{tel_links('<span aria-hidden="true">·</span>')}</p>
  </div>
</section>'''

def page_hero(ctx, eyebrow, title, lede="", cls=""):
    l = f'<p class="page-hero__lede rise" style="--d:160ms">{esc(lede)}</p>' if lede else ""
    return f'''<section class="page-hero {cls}">
  <div class="wrap">
    <p class="eyebrow rise">{esc(eyebrow)}</p>
    <h1 class="h1 rise" style="--d:80ms">{esc(title)}</h1>
    {l}
  </div>
</section>'''

# ----------------------------------------------------------------- home ----
def hero(ctx):
    t = ctx.t
    slides, bars = [], []
    for k, (slug, n, _, _) in enumerate(C.HERO):
        wide, tall = MAN[f"hero-{k}-wide"], MAN[f"hero-{k}-tall"]
        ws, ts = srcset(ctx, f"hero-{k}-wide"), srcset(ctx, f"hero-{k}-tall")
        alt = esc(label(ctx, f"{slug}-{n:02d}"))
        r = ROOM[slug]
        data = f'data-name="{esc(r["name"])}" data-href="{ctx.url("rooms/" + slug + "/")}"'
        if k == 0:
            slides.append(f'''<div class="hero__slide is-active" {data}>
      <picture><source media="(max-width: 760px)" srcset="{ts}" sizes="100vw">
      <img src="{src_near(ctx, f"hero-{k}-wide", 1920)}" srcset="{ws}" sizes="100vw" width="{wide["w"]}" height="{wide["h"]}" alt="{alt}" fetchpriority="high" decoding="async" style="background-color:{wide["color"]}"></picture>
    </div>''')
        else:
            slides.append(f'''<div class="hero__slide" {data}>
      <picture><source media="(max-width: 760px)" data-srcset="{ts}" sizes="100vw">
      <img src="{BLANK}" data-srcset="{ws}" sizes="100vw" width="{wide["w"]}" height="{wide["h"]}" alt="{alt}" decoding="async" style="background-color:{wide["color"]}"></picture>
    </div>''')
        bars.append(f'<button type="button" aria-label="{esc(t["slide"])} {k + 1}: {esc(r["name"])}"{" aria-current=true" if k == 0 else ""}><i></i></button>')
    first = ROOM[C.HERO[0][0]]
    return f'''<section class="hero" data-hero>
  <div class="hero__slides">
    {"".join(slides)}
  </div>
  <div class="hero__shade"></div>
  <div class="hero__inner">
    <div class="hero__copy">
      <p class="eyebrow eyebrow--line hero__in" style="--d:.15s">{esc(t["hero_eyebrow"])}</p>
      <h1 class="hero__title hero__in" style="--d:.3s">{t["hero_title"]}</h1>
      <div class="hero__row hero__in" style="--d:.5s">
        <p class="hero__lede">{esc(t["hero_lede"])}</p>
        <div class="btn-row">
          <a class="btn btn--light" href="#lofts">{esc(t["hero_cta"])} {ICON["down"]}</a>
          <a class="btn btn--ghost-light" href="{ctx.booking}" target="_blank" rel="noopener">{esc(t["book"])} {ICON["out"]}</a>
        </div>
      </div>
    </div>
    <div class="hero__meta hero__in" style="--d:.7s">
      <a class="hero__cap" href="{ctx.url("rooms/" + first["slug"] + "/")}" data-hero-link>
        <span class="num" data-hero-num>01</span><span class="hero__capname" data-hero-name>{esc(first["name"])}</span>{ICON["arrow"]}
      </a>
      <div class="hero__bars" data-hero-bars>{"".join(bars)}</div>
    </div>
  </div>
</section>'''

def home(ctx):
    t = ctx.t
    stats = "".join(f'<li data-reveal style="--d:{i * 90}ms"><strong>{esc(t[f"stat_{i + 1}"][0])}</strong><span>{esc(t[f"stat_{i + 1}"][1])}</span></li>' for i in range(4))
    words = "".join(f"<span>{esc(w)}</span><i></i>" for w in t["marquee"])
    peek_ids = ["executive-loft-iii-04", "roof-lounge", "eclectic-style-apartment-04", "executive-loft-iv-02", "separated-premium-room-02"]
    peek_ratio = ["45", "43", "11", "11", "43"]
    peek_sizes = ["(min-width: 760px) 40vw, 100vw"] + ["(min-width: 760px) 32vw, 50vw"] * 4
    peek = [lb(ctx, iid, frame(ctx, iid, peek_sizes[i], peek_ratio[i]), "peek", "peek__item") for i, iid in enumerate(peek_ids)]
    quotes = []
    for i, q in enumerate(C.REVIEWS):
        text, qlang, note = q["text"], q["lang"], ""
        name = q["name"]
        if ctx.lang == "en" and q["lang"] != "en":
            text, qlang, name = q["text_en"], "en", q.get("name_en", q["name"])
            note = f'<span class="quote__note">{esc(t["translated"])}</span>'
        quotes.append(f'''<figure class="quote" data-reveal style="--d:{i * 110}ms">
        <blockquote lang="{qlang}"><p>{esc(text)}</p></blockquote>
        <figcaption><strong>{esc(name)}</strong><span>{esc(q["from"][ctx.lang])}</span>{note}</figcaption>
      </figure>''')
    body = f'''{hero(ctx)}

<section class="welcome sec" id="welcome">
  <div class="wrap welcome__grid">
    <div class="welcome__text">
      <p class="eyebrow" data-reveal>{esc(t["welcome_eyebrow"])}</p>
      <h2 class="h2" data-reveal style="--d:80ms">{esc(t["welcome_title"])}</h2>
      <p class="lede" data-reveal style="--d:160ms">{esc(t["welcome_p"])}</p>
      <p data-reveal style="--d:240ms"><a class="link" href="{ctx.url("about/")}">{esc(t["welcome_link"])} {ICON["arrow"]}</a></p>
    </div>
    <div class="welcome__media">
      {frame(ctx, "ext-entrance", SZ_HALF, "45", "welcome__a")}
      {frame(ctx, "ext-dusk", SZ_QUARTER, "11", "welcome__b", attrs=" data-parallax")}
      <p class="welcome__cap">{esc(t["welcome_caption"])}</p>
    </div>
  </div>
  <div class="wrap"><ul class="stats">{stats}</ul></div>
</section>

<section class="lofts sec theme-dark" id="lofts">
  <div class="wrap lofts__head">
    <div data-reveal>
      <p class="eyebrow">{esc(t["rooms_eyebrow"])}</p>
      <h2 class="h2">{esc(t["rooms_title"])}</h2>
    </div>
    <div class="lofts__intro" data-reveal style="--d:120ms">
      <p>{esc(t["rooms_intro"])}</p>
      {rail_nav(ctx)}
    </div>
  </div>
  {rail(ctx, C.ROOMS, t["rooms_title"])}
  <div class="wrap lofts__foot">
    <div class="rail-progress" aria-hidden="true"><i data-rail-bar></i></div>
    <a class="link" href="{ctx.url("rooms/")}">{esc(t["rooms_all"])} {ICON["arrow"]}</a>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{words * 4}</div></div>

<section class="house sec">
  <div class="wrap house__a">
    {frame(ctx, "roof-deck", SZ_HALF, "43", "house__big")}
    <div class="house__text" data-reveal>
      <p class="eyebrow">{esc(t["house_eyebrow"])}</p>
      <h2 class="h2">{esc(t["roof_title"])}</h2>
      <p>{esc(t["roof_p"])}</p>
      <p><a class="link" href="{ctx.url("about/")}">{esc(t["house_link"])} {ICON["arrow"]}</a></p>
    </div>
  </div>
  <div class="wrap house__b">
    <div class="house__text house__text--b" data-reveal>
      <h3 class="h3">{esc(t["gym_title"])}</h3>
      <p>{esc(t["gym_p"])}</p>
    </div>
    {frame(ctx, "roof-view", SZ_QUARTER, "45", "house__tall", attrs=" data-parallax")}
    {frame(ctx, "gym-room", SZ_THIRD, "43", "house__gym")}
  </div>
</section>

{amenities(ctx, C.COMMON_FACILITIES)}

<section class="peek sec">
  <div class="wrap sec-head sec-head--row">
    <div data-reveal>
      <p class="eyebrow">{esc(t["gal_eyebrow"])}</p>
      <h2 class="h2">{esc(t["gal_title"])}</h2>
    </div>
    <a class="link" href="{ctx.url("gallery/")}" data-reveal>{esc(t["gal_link"])} {ICON["arrow"]}</a>
  </div>
  <div class="wrap peek__grid">
    <div class="peek__col">{peek[0]}</div>
    <div class="peek__col peek__col--mid">{peek[1]}{peek[2]}</div>
    <div class="peek__col">{peek[3]}{peek[4]}</div>
  </div>
</section>

<section class="guests sec">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      <p class="eyebrow">{esc(t["guests_eyebrow"])}</p>
      <h2 class="h2">{esc(t["guests_title"])}</h2>
    </header>
    <div class="guests__grid">
      {"".join(quotes)}
    </div>
  </div>
</section>

{location(ctx)}
{cta(ctx)}'''
    k0w, k0t = MAN["hero-0-wide"], MAN["hero-0-tall"]
    preload = (f'<link rel="preload" as="image" imagesrcset="{srcset(ctx, "hero-0-tall")}" imagesizes="100vw" media="(max-width: 760px)" fetchpriority="high">\n'
               f'<link rel="preload" as="image" imagesrcset="{srcset(ctx, "hero-0-wide")}" imagesizes="100vw" media="(min-width: 761px)" fetchpriority="high">\n')
    ld = {
        "@context": "https://schema.org", "@type": "LodgingBusiness", "name": "Allofts",
        "description": t["home_meta_desc"], "url": ctx.abs(), "email": C.SITE["email"],
        "telephone": C.SITE["phones"][0][0],
        "image": [C.SITE["url"] + "/assets/img/og.jpg"],
        "address": {"@type": "PostalAddress", "streetAddress": C.SITE["address"][ctx.lang][0], "addressLocality": "Kalamata" if ctx.lang == "en" else "Καλαμάτα",
                    "postalCode": "24100", "addressCountry": "GR"},
        "sameAs": [C.SITE["instagram"], C.SITE["facebook"]],
        "numberOfRooms": len(C.ROOMS),
    }
    return page(ctx, t["home_meta_title"], t["home_meta_desc"], body, "top-dark page-home", "", preload=preload, jsonld=ld)

# ---------------------------------------------------------------- rooms ----
def rooms_index(ctx):
    t = ctx.t
    rows = []
    for r in C.ROOMS:
        href = ctx.url("rooms/" + r["slug"] + "/")
        inset = next((i for i, (_, tag) in enumerate(r["photos"], 1) if i > 1 and tag in ("bedroom", "garden", "net")), 2)
        sp = "".join(f"<li>{esc(s)}</li>" for s in specs(ctx, r))
        rows.append(f'''<article class="row">
    <a class="row__media" href="{href}" tabindex="-1" aria-hidden="true">
      {frame(ctx, room_id(r), SZ_HALF, "32", "row__main")}
      {frame(ctx, room_id(r, inset), SZ_QUARTER, "45", "row__inset")}
    </a>
    <div class="row__body" data-reveal>
      <p class="eyebrow"><span class="num">{room_no(r)}</span>{esc(t["kind"][r["kind"]])}</p>
      <h2 class="h2 row__name"><a href="{href}">{esc(r["name"])}</a></h2>
      <p class="row__tag">{esc(r["tagline"][ctx.lang])}</p>
      <ul class="specs">{sp}</ul>
      <div class="row__foot">
        <p class="price">{esc(price(ctx, r))} <span>{esc(t["per_night"])}</span></p>
        <a class="link" href="{href}">{esc(t["discover"])} {ICON["arrow"]}</a>
      </div>
    </div>
  </article>''')
    body = f'''{page_hero(ctx, t["rooms_eyebrow"], t["rooms_page_title"], t["rooms_page_lede"])}
<section class="rows">
  <div class="wrap">
  {"".join(rows)}
  </div>
</section>
{cta(ctx)}'''
    return page(ctx, t["rooms_meta_title"], t["rooms_meta_desc"], body, "top-light", "rooms/")

def room_page(ctx, r):
    t = ctx.t
    n = len(r["photos"])
    group = r["slug"]
    ids = [room_id(r, i) for i in range(1, n + 1)]
    mosaic = "".join(
        lb(ctx, iid, img(ctx, iid, SZ_HALF if i == 0 else SZ_QUARTER, lazy=i > 0), group, f"mosaic__item mosaic__item--{i + 1}")
        for i, iid in enumerate(ids[:5]))
    more = "".join(lb(ctx, iid, frame(ctx, iid, SZ_MASONRY, "", "", reveal=False, attrs=f' style="aspect-ratio:{MAN[iid]["w"]}/{MAN[iid]["h"]}"'), group, "masonry__item") for iid in ids[5:])
    kind = t["kind"][r["kind"]]
    facts = [(t["size"], size(ctx, r)), (t["guests"], t["upto_short"].format(n=r["guests"])), (t["bed"], t["bed_queen_short"])]
    if r["extra"]: facts.append(("+", C.EXTRA[r["extra"]][ctx.lang]))
    if r["sofa"]: facts.append(("+", t[f"sofa_{r['sofa']}"]))
    facts_html = "".join(f"<li><span>{esc(a)}</span><strong>{esc(b)}</strong></li>" for a, b in facts)
    fac = "".join(f"<li>{esc(C.FACILITIES[k][ctx.lang])}</li>" for k in r["facilities"])
    idx = C.ROOMS.index(r)
    prev_r, next_r = C.ROOMS[idx - 1], C.ROOMS[(idx + 1) % len(C.ROOMS)]
    def pager(rr, key, cls):
        return f'''<a class="pager__item {cls}" href="{ctx.url("rooms/" + rr["slug"] + "/")}">
      <span class="pager__img">{img(ctx, room_id(rr), SZ_HALF, alt="")}</span>
      <span class="pager__text"><span class="eyebrow">{esc(t[key])}</span><span class="pager__name">{esc(rr["name"])}</span></span>
    </a>'''
    ask = t["book_ask"].format(kind=kind.lower())
    body = f'''<article class="room">
  <header class="room-head wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{ctx.url("rooms/")}">{esc(t["nav_rooms"])}</a><span aria-hidden="true">/</span><span aria-current="page">{esc(r["name"])}</span></nav>
    <div class="room-head__grid">
      <div>
        <p class="eyebrow rise"><span class="num">{room_no(r)}</span>{esc(kind)}</p>
        <h1 class="h1 rise" style="--d:80ms">{esc(r["name"])}</h1>
      </div>
      <p class="room-head__tag rise" style="--d:160ms">{esc(r["tagline"][ctx.lang])}</p>
    </div>
  </header>

  <div class="shots wrap">
    <div class="mosaic">{mosaic}</div>
    <button class="btn btn--paper shots__more" type="button" data-lb-open="{group}">{esc(t["all_photos"].format(n=n))}</button>
  </div>

  <div class="wrap room-body">
    <div class="room-main">
      <ul class="facts">{facts_html}</ul>
      <h2 class="h3">{esc(t["about_room"])}</h2>
      <div class="prose">{"".join(f"<p>{esc(p)}</p>" for p in r["desc"][ctx.lang])}</div>
      <h2 class="h3">{esc(t["facilities"])}</h2>
      <ul class="fac">{fac}</ul>
    </div>
    <aside class="bookcard">
      <p class="eyebrow">{esc(t["book_title"])}</p>
      <p class="bookcard__price"><span>{esc(t["from"])}</span> €{r.get("price", C.SITE["price_from"])} <small>{esc(t["per_night"])}</small></p>
      <a class="btn btn--solid btn--block" href="{ctx.booking}" target="_blank" rel="noopener">{esc(t["book_booking"])} {ICON["out"]}</a>
      <a class="btn btn--ghost btn--block" href="{ctx.url("contact/")}?room={r["slug"]}">{esc(ask)}</a>
      <p class="bookcard__note">{esc(t["book_note"])}</p>
      <p class="bookcard__contact">{tel_links("<br>")}<br><a href="mailto:{C.SITE["email"]}">{C.SITE["email"]}</a></p>
    </aside>
  </div>

  <section class="more wrap">
    <h2 class="h3">{esc(t["more_photos"].format(name=r["name"]))}</h2>
    <div class="masonry">{more}</div>
  </section>

  <nav class="pager" aria-label="{esc(t["all_rooms"])}">
    {pager(prev_r, "prev_room", "pager__item--prev")}
    {pager(next_r, "next_room", "pager__item--next")}
  </nav>
</article>
{cta(ctx)}'''
    desc = f"{r['name']}: {r['tagline'][ctx.lang]} {size(ctx, r)}, {t['upto'].format(n=r['guests']).lower()}. Allofts, {'Kalamata' if ctx.lang == 'en' else 'Καλαμάτα'}."
    m = MAN[room_id(r)]
    og = f"{C.SITE['url']}/assets/{m['base']}-{m['variants'][min(2, len(m['variants']) - 1)][0]}.webp"
    title = f"{r['name']}, {kind.lower()} {t['in_city']}"
    return page(ctx, title, desc, body, "top-light page-room", "rooms/", og=og)

# -------------------------------------------------------------- gallery ----
def gallery(ctx):
    t = ctx.t
    items = []
    for cat, ref in C.GALLERY:
        iid = ref if isinstance(ref, str) else f"{ref[0]}-{ref[1]:02d}"
        m = MAN[iid]
        room = IMAGES[iid]["room"]
        cap = ROOM[room]["name"] if room else t["tags"][IMAGES[iid]["tag"]]
        inner = (f'<figure class="frame" style="aspect-ratio:{m["w"]}/{m["h"]}">{img(ctx, iid, SZ_MASONRY)}</figure>'
                 f'<span class="gallery__cap">{esc(cap)}</span>')
        items.append(lb(ctx, iid, inner, "gallery", "gallery__item", f' data-cat="{cat}"'))
    chips = "".join(f'<button class="chip{" is-active" if k == "all" else ""}" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{esc(t["f_" + k])}</button>'
                    for k in ("all", "lofts", "house", "roof"))
    body = f'''{page_hero(ctx, t["gal_eyebrow"], t["gallery_page_title"], t["gallery_page_lede"])}
<section class="gallery-sec">
  <div class="wrap">
    <div class="chips" role="group" aria-label="{esc(t["gallery_page_title"])}" data-filters>{chips}</div>
    <div class="gallery" data-gallery>
      {"".join(items)}
    </div>
  </div>
</section>
{cta(ctx)}'''
    return page(ctx, t["gallery_page_title"], t["gallery_meta_desc"], body, "top-light", "gallery/")

# ---------------------------------------------------------------- about ----
def about(ctx):
    t = ctx.t
    ps = t["about_ps"]
    verbs = "".join(f'<li data-reveal style="--d:{i * 90}ms"><span class="num">{i + 1:02d}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for i, (a, b) in enumerate(t["verbs"]))
    roof_ids = ["roof-table", "roof-lounge", "roof-view", "roof-sunset", "roof-bar", "roof-wide", "roof-drone", "roof-moon"]
    roof = "".join(lb(ctx, iid, frame(ctx, iid, SZ_CARD, "45", "", reveal=False), "roof", "rail__photo") for iid in roof_ids)
    body = f'''<section class="about-hero">
  <div class="wrap about-hero__grid">
    <div class="about-hero__text">
      <p class="eyebrow rise">{esc(t["about_eyebrow"])}</p>
      <h1 class="h1 rise" style="--d:80ms">{t["hero_title"]}</h1>
      <p class="lede rise" style="--d:160ms">{esc(ps[0])}</p>
    </div>
    {frame(ctx, "ext-day", SZ_HALF, "45", "about-hero__img", lazy=False)}
  </div>
</section>

<section class="story sec">
  <div class="wrap story__grid">
    {frame(ctx, "ext-dusk", SZ_THIRD, "11", "story__img", attrs=" data-parallax")}
    <div class="prose prose--lg" data-reveal>
      {"".join(f"<p>{esc(p)}</p>" for p in ps[1:])}
      <p><a class="link" href="{ctx.url("rooms/")}">{esc(t["rooms_all"])} {ICON["arrow"]}</a></p>
    </div>
  </div>
</section>

<section class="verbs sec theme-dark">
  <div class="wrap">
    <header class="sec-head" data-reveal>
      <p class="eyebrow">{esc(t["tagline"])}</p>
      <h2 class="h2">{esc(t["verbs_title"])}</h2>
    </header>
    <ul class="verbs__grid">{verbs}</ul>
  </div>
</section>

<section class="roof sec">
  <div class="wrap roof__head">
    <div data-reveal>
      <p class="eyebrow">{esc(t["about_roof_eyebrow"])}</p>
      <h2 class="h2">{esc(t["roof_title"])}</h2>
    </div>
    <div class="roof__intro" data-reveal style="--d:120ms">
      <p>{esc(t["roof_p"])}</p>
      {rail_nav(ctx)}
    </div>
  </div>
  <div class="rail rail--photos" data-rail tabindex="0" role="region" aria-label="{esc(t["roof_title"])}">{roof}</div>
</section>

<section class="duo sec">
  <div class="wrap duo__grid">
    <div class="duo__item">
      {lb(ctx, "gym-room", frame(ctx, "gym-room", SZ_HALF, "43"), "house")}
      <div data-reveal>
        <p class="eyebrow">{esc(t["about_gym_eyebrow"])}</p>
        <h2 class="h3">{esc(t["gym_title"])}</h2>
        <p>{esc(t["gym_p"])}</p>
      </div>
    </div>
    <div class="duo__item duo__item--b">
      {lb(ctx, "in-corridor", frame(ctx, "in-corridor", SZ_HALF, "43"), "house")}
      <div data-reveal>
        <p class="eyebrow">{esc(t["about_building_eyebrow"])}</p>
        <h2 class="h3">{esc(t["about_building_title"])}</h2>
        <p>{esc(t["about_building_p"])}</p>
      </div>
    </div>
  </div>
</section>

{amenities(ctx, C.COMMON_FACILITIES)}
{location(ctx)}
{cta(ctx)}'''
    return page(ctx, t["about_meta_title"], t["about_meta_desc"], body, "top-light", "about/")

# -------------------------------------------------------------- contact ----
def contact(ctx):
    t = ctx.t
    addr = "<br>".join(esc(a) for a in C.SITE["address"][ctx.lang])
    opts = "".join(f'<option value="{r["slug"]}">{esc(r["name"])}</option>' for r in C.ROOMS)
    labels = esc(json.dumps({"subject": t["form_subject"], "required": t["form_required"], **t["mail_labels"]}, ensure_ascii=False))
    body = f'''{page_hero(ctx, t["contact_eyebrow"], t["contact_title"], t["contact_p"])}
<section class="contact">
  <div class="wrap contact__grid">
    <div class="contact__info" data-reveal>
      <dl class="info">
        <div><dt>{esc(t["c_address"])}</dt><dd><address>{addr}</address><a class="ul" href="{C.SITE["maps_link"]}" target="_blank" rel="noopener">{esc(t["loc_maps"])}</a></dd></div>
        <div><dt>{esc(t["c_phones"])}</dt><dd>{tel_links("<br>")}</dd></div>
        <div><dt>{esc(t["c_email"])}</dt><dd><a class="ul" href="mailto:{C.SITE["email"]}">{C.SITE["email"]}</a></dd></div>
        <div><dt>{esc(t["c_social"])}</dt><dd><a class="ul" href="{C.SITE["instagram"]}" target="_blank" rel="noopener">Instagram</a><br><a class="ul" href="{C.SITE["facebook"]}" target="_blank" rel="noopener">Facebook</a></dd></div>
      </dl>
      <a class="btn btn--solid" href="{ctx.booking}" target="_blank" rel="noopener">{esc(t["book_booking"])} {ICON["out"]}</a>
    </div>
    <form class="form" action="mailto:{C.SITE["email"]}" method="post" enctype="text/plain" data-enquiry data-to="{C.SITE["email"]}" data-labels="{labels}" novalidate data-reveal>
      <h2 class="h3">{esc(t["form_title"])}</h2>
      <div class="form__grid">
        <div class="field"><label for="f-name">{esc(t["form_name"])} *</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
        <div class="field"><label for="f-email">{esc(t["form_email"])} *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="f-phone">{esc(t["form_phone"])}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="f-room">{esc(t["form_room"])}</label><select id="f-room" name="room"><option value="">{esc(t["form_any"])}</option>{opts}</select></div>
        <div class="field field--third"><label for="f-in">{esc(t["form_in"])}</label><input id="f-in" name="in" type="date"></div>
        <div class="field field--third"><label for="f-out">{esc(t["form_out"])}</label><input id="f-out" name="out" type="date"></div>
        <div class="field field--third"><label for="f-guests">{esc(t["form_guests"])}</label><select id="f-guests" name="guests"><option>1</option><option selected>2</option><option>3</option><option>4</option></select></div>
        <div class="field field--full"><label for="f-msg">{esc(t["form_msg"])}</label><textarea id="f-msg" name="msg" rows="4" placeholder="{esc(t["form_msg_ph"])}"></textarea></div>
      </div>
      <p class="form__error" role="alert" hidden></p>
      <div class="form__foot">
        <button class="btn btn--solid" type="submit">{esc(t["form_send"])} {ICON["arrow"]}</button>
        <p class="form__hint">{esc(t["form_hint"])}</p>
      </div>
      <p class="form__done" role="status" hidden>{esc(t["form_done"])}</p>
    </form>
  </div>
</section>
{location(ctx)}'''
    return page(ctx, t["contact_meta_title"], t["contact_meta_desc"], body, "top-light", "contact/")

def privacy(ctx):
    t = ctx.t
    items = "".join(f"<h2>{esc(a)}</h2><p>{esc(b)}</p>" for a, b in t["privacy_items"])
    body = f'''{page_hero(ctx, "Allofts", t["privacy_title"], t["privacy_intro"])}
<section class="legal"><div class="wrap"><div class="prose">{items}</div></div></section>'''
    return page(ctx, t["privacy_title"], t["privacy_meta_desc"], body, "top-light", "")

def not_found():
    ctx = Ctx("en", "", absolute=True)
    t, el = ctx.t, C.T["el"]
    body = f'''<section class="page-hero page-hero--center">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1 class="h1">{esc(t["nf_title"])}</h1>
    <p class="page-hero__lede">{esc(t["nf_p"])}</p>
    <p class="btn-row btn-row--center"><a class="btn btn--solid" href="/">{esc(t["nf_home"])}</a><a class="btn btn--ghost" href="/el/" lang="el">{esc(el["nf_home"])}</a></p>
  </div>
</section>'''
    return page(ctx, t["nf_title"], t["nf_p"], body, "top-light", "").replace('<meta name="theme-color"', '<meta name="robots" content="noindex">\n<meta name="theme-color"', 1)

def stub(lang, old_path, new_path):
    """A tiny page at an address of the old website that forwards visitors to the new one."""
    prefix = "" if lang == "en" else "el/"
    rel = "../" * (prefix + old_path).count("/") + prefix + new_path
    absu = C.SITE["url"] + "/" + prefix + new_path
    write(prefix + old_path + "index.html",
          f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n<title>Allofts</title>\n<meta name="robots" content="noindex">\n'
          f'<link rel="canonical" href="{absu}">\n<meta http-equiv="refresh" content="0; url={rel}">\n</head>\n'
          f'<body>\n<p><a href="{rel}">{esc(C.T[lang]["moved"])}</a></p>\n</body>\n</html>\n')

# ----------------------------------------------------------------- main ----
def main():
    if "--clean" in sys.argv and os.path.exists(OUT):
        shutil.rmtree(OUT)
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
    os.makedirs(OUT, exist_ok=True)
    print("photos")
    register_images()
    build_images()
    print("static files")
    for sub in ("css", "js", "fonts", "img"):
        src, dst = os.path.join(HERE, "static", sub), os.path.join(OUT, "assets", sub)
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src): shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
    print("pages")
    pages = []
    for lang in C.LANGS:
        def emit(path, fn, *a):
            ctx = Ctx(lang, path)
            write(ctx.prefix + path + "index.html", fn(ctx, *a))
            pages.append((lang, path))
        emit("", home)
        emit("rooms/", rooms_index)
        for r in C.ROOMS: emit(f"rooms/{r['slug']}/", room_page, r)
        emit("gallery/", gallery)
        emit("about/", about)
        emit("contact/", contact)
        emit("privacy-policy/", privacy)
        # addresses of the old website keep working
        for r in C.ROOMS: stub(lang, f"hotel_room/{r['slug']}/", f"rooms/{r['slug']}/")
        stub(lang, "st_hotel/allofts/", "about/")
    write("404.html", not_found())
    # sitemap, robots, manifest
    base = C.SITE["url"] + "/"
    urls = []
    for lang, path in pages:
        if lang != "en": continue
        urls.append(f'  <url><loc>{base}{path}</loc><xhtml:link rel="alternate" hreflang="en" href="{base}{path}"/>'
                    f'<xhtml:link rel="alternate" hreflang="el" href="{base}el/{path}"/></url>\n'
                    f'  <url><loc>{base}el/{path}</loc><xhtml:link rel="alternate" hreflang="en" href="{base}{path}"/>'
                    f'<xhtml:link rel="alternate" hreflang="el" href="{base}el/{path}"/></url>')
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": "Allofts — Contemporary Living", "short_name": "Allofts", "start_url": "/", "display": "browser",
        "background_color": "#131417", "theme_color": "#131417",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    n_img = sum(len(m["variants"]) for m in MAN.values())
    print(f"done: {len(pages)} pages, {len(MAN)} photos in {n_img} sizes -> {OUT}")

if __name__ == "__main__":
    main()
