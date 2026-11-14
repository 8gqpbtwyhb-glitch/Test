/* Allofts — small, dependency-free interactions.
   header · menu · home slideshow · scroll reveals · carousels · photo viewer ·
   gallery filters · map on request · enquiry form */
(function () {
  'use strict';
  window.__allofts = true;

  var doc = document, body = doc.body;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(f, 16); };

  function throttle(fn) {
    var busy = false;
    return function () { if (busy) return; busy = true; raf(function () { busy = false; fn(); }); };
  }

  /* When the site is opened straight from a folder (no web server), folder links need "index.html". */
  var local = location.protocol === 'file:';
  function fix(href) {
    if (!local || !href || /^([a-z][a-z0-9+.-]*:|#|\/\/)/i.test(href)) return href;
    var m = href.match(/^([^?#]*)(.*)$/);
    return /\/$/.test(m[1]) ? m[1] + 'index.html' + m[2] : href;
  }
  if (local) $$('a[href]').forEach(function (a) { a.setAttribute('href', fix(a.getAttribute('href'))); });

  /* ---------------------------------------------------------- header ---- */
  var header = $('[data-header]'), dock = $('[data-dock]'), footer = $('.site-footer');
  var lastY = window.scrollY, footerSeen = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle('is-solid', y > 24);
      if (y > lastY + 6 && y > 520) header.classList.add('is-hidden');
      else if (y < lastY - 6 || y <= 520) header.classList.remove('is-hidden');
    }
    if (dock) dock.classList.toggle('is-on', y > window.innerHeight * 0.7 && !footerSeen);
    lastY = y;
  }
  window.addEventListener('scroll', throttle(onScroll), { passive: true });
  onScroll();
  if (header) header.addEventListener('focusin', function () { header.classList.remove('is-hidden'); });
  if (footer && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { footerSeen = es[0].isIntersecting; onScroll(); }, { rootMargin: '0px 0px -120px 0px' }).observe(footer);
  }

  /* ------------------------------------------------------------ menu ---- */
  var burger = $('[data-burger]'), menu = $('[data-menu]');
  function setMenu(open) {
    body.classList.toggle('menu-open', open);
    body.classList.toggle('is-locked', open);
    burger.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-hidden', String(!open));
    if (open) header.classList.remove('is-hidden');
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(!body.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    doc.addEventListener('keydown', function (e) {
      if (!body.classList.contains('menu-open')) return;
      if (e.key === 'Escape') { setMenu(false); burger.focus(); }
      if (e.key === 'Tab') {                         // keep the keyboard inside the open menu
        var f = [burger].concat($$('a', menu)), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    window.addEventListener('resize', throttle(function () { if (window.innerWidth > 1020 && body.classList.contains('menu-open')) setMenu(false); }));
  }

  /* --------------------------------------------------- home slideshow ---- */
  var hero = $('[data-hero]');
  if (hero) {
    var slides = $$('.hero__slide', hero), bars = $$('[data-hero-bars] button', hero);
    var hNum = $('[data-hero-num]', hero), hName = $('[data-hero-name]', hero), hLink = $('[data-hero-link]', hero);
    var cur = 0, timer = null, DUR = 7000;
    var hydrate = function (slide) {
      $$('[data-srcset]', slide).forEach(function (el) { el.setAttribute('srcset', el.getAttribute('data-srcset')); el.removeAttribute('data-srcset'); });
    };
    var go = function (i) {
      i = (i + slides.length) % slides.length;
      if (i === cur) return;
      hydrate(slides[i]);
      slides[cur].classList.remove('is-active'); bars[cur].removeAttribute('aria-current');
      cur = i;
      slides[cur].classList.add('is-active'); bars[cur].setAttribute('aria-current', 'true');
      hNum.textContent = ('0' + (cur + 1)).slice(-2);
      hName.textContent = slides[cur].getAttribute('data-name');
      hLink.setAttribute('href', fix(slides[cur].getAttribute('data-href')));
      hydrate(slides[(cur + 1) % slides.length]);
    };
    var play = function () { clearInterval(timer); if (!reduce && slides.length > 1) timer = setInterval(function () { go(cur + 1); }, DUR); };
    bars.forEach(function (b, i) { b.addEventListener('click', function () { go(i); play(); }); });
    var start = function () { if (slides[1]) hydrate(slides[1]); play(); };
    if (doc.readyState === 'complete') start(); else window.addEventListener('load', start);
    doc.addEventListener('visibilitychange', function () { if (doc.hidden) clearInterval(timer); else play(); });
    var hx = null;
    hero.addEventListener('touchstart', function (e) { hx = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      if (hx === null) return;
      var dx = e.changedTouches[0].clientX - hx; hx = null;
      if (Math.abs(dx) > 60) { go(cur + (dx < 0 ? 1 : -1)); play(); }
    }, { passive: true });
  }

  /* --------------------------------------------------- scroll reveals ---- */
  /* Measured by hand rather than with IntersectionObserver: the photos start fully clipped,
     and a fully clipped element never counts as "visible" to an observer. */
  var pending = $$('[data-reveal]');
  var reveal = function () {
    if (!pending.length) return;
    var edge = window.innerHeight * 0.93;
    pending = pending.filter(function (el) {
      if (el.getBoundingClientRect().top > edge) return true;
      el.classList.add('is-in');
      return false;
    });
  };
  window.addEventListener('scroll', throttle(reveal), { passive: true });
  window.addEventListener('resize', throttle(reveal));
  window.addEventListener('load', reveal);
  reveal();

  /* gentle drift on a few layered photos */
  var par = $$('[data-parallax]');
  if (par.length && !reduce && 'IntersectionObserver' in window) {
    var live = [];
    var drift = function () {
      var vh = window.innerHeight;
      live.forEach(function (el) {
        var r = (el.parentElement || el).getBoundingClientRect();
        var p = (r.top + r.height / 2 - vh / 2) / vh;
        el.style.setProperty('--py', (Math.max(-1, Math.min(1, p)) * -42).toFixed(1) + 'px');
      });
    };
    var pio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var i = live.indexOf(e.target);
        if (e.isIntersecting && i < 0) live.push(e.target);
        if (!e.isIntersecting && i >= 0) live.splice(i, 1);
      });
      drift();
    }, { rootMargin: '25% 0px' });
    par.forEach(function (el) { pio.observe(el); });
    window.addEventListener('scroll', throttle(drift), { passive: true });
    window.addEventListener('resize', throttle(drift));
  }

  /* -------------------------------------------------------- carousels ---- */
  $$('[data-rail]').forEach(function (rail) {
    var scope = rail.closest('section') || doc;
    var prev = $('[data-rail-prev]', scope), next = $('[data-rail-next]', scope), bar = $('[data-rail-bar]', scope);
    var stepSize = function () {
      var c = rail.children[0];
      return c ? c.getBoundingClientRect().width + (parseFloat(getComputedStyle(rail).columnGap) || 0) : rail.clientWidth * 0.8;
    };
    var update = function () {
      var max = rail.scrollWidth - rail.clientWidth, p = max > 0 ? rail.scrollLeft / max : 0;
      if (prev) prev.disabled = rail.scrollLeft < 8;
      if (next) next.disabled = rail.scrollLeft > max - 8;
      if (bar) {
        var w = Math.min(1, Math.max(0.12, rail.clientWidth / rail.scrollWidth));
        bar.style.width = (w * 100) + '%';
        bar.style.transform = 'translateX(' + (p * (1 - w) / w * 100) + '%)';
      }
    };
    var move = function (dir) { rail.scrollBy({ left: dir * stepSize() * (window.innerWidth > 1000 ? 2 : 1), behavior: reduce ? 'auto' : 'smooth' }); };
    if (prev) prev.addEventListener('click', function () { move(-1); });
    if (next) next.addEventListener('click', function () { move(1); });
    rail.addEventListener('scroll', throttle(update), { passive: true });
    window.addEventListener('resize', throttle(update));
    update();

    // drag with the mouse
    var down = false, moved = false, sx = 0, sl = 0;
    rail.addEventListener('mousedown', function (e) { if (e.button !== 0) return; down = true; moved = false; sx = e.clientX; sl = rail.scrollLeft; });
    window.addEventListener('mousemove', function (e) {
      if (!down) return;
      var dx = e.clientX - sx;
      if (!moved && Math.abs(dx) > 6) { moved = true; rail.classList.add('is-dragging'); }
      if (moved) rail.scrollLeft = sl - dx;
    });
    window.addEventListener('mouseup', function () {
      if (!down) return;
      down = false;
      if (!moved) return;
      var s = stepSize(), target = Math.round(rail.scrollLeft / s) * s;
      rail.scrollTo({ left: target, behavior: reduce ? 'auto' : 'smooth' });
      setTimeout(function () { rail.classList.remove('is-dragging'); }, 420);
    });
    rail.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
    rail.addEventListener('dragstart', function (e) { e.preventDefault(); });
  });

  /* ----------------------------------------------------- photo viewer ---- */
  var lbItems = $$('a.lb');
  if (lbItems.length) {
    var isEl = doc.documentElement.lang === 'el';
    var L = isEl ? { close: 'Κλείσιμο', prev: 'Προηγούμενη φωτογραφία', next: 'Επόμενη φωτογραφία', title: 'Φωτογραφίες' }
                 : { close: 'Close', prev: 'Previous photo', next: 'Next photo', title: 'Photos' };
    var arrow = function (d) { return '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="' + d + '"/></svg>'; };
    var lbx = doc.createElement('div');
    lbx.className = 'lbx';
    lbx.setAttribute('role', 'dialog'); lbx.setAttribute('aria-modal', 'true'); lbx.setAttribute('aria-label', L.title); lbx.setAttribute('aria-hidden', 'true');
    lbx.innerHTML =
      '<div class="lbx__bar"><span class="lbx__count" aria-live="polite"></span>' +
      '<button class="lbx__close" type="button" aria-label="' + L.close + '">' + arrow('M6 6l12 12M18 6 6 18') + '</button></div>' +
      '<div class="lbx__stage"><button class="lbx__nav lbx__nav--prev" type="button" aria-label="' + L.prev + '">' + arrow('M20 12H5M11 6l-6 6 6 6') + '</button>' +
      '<img class="lbx__img" alt="" draggable="false">' +
      '<button class="lbx__nav lbx__nav--next" type="button" aria-label="' + L.next + '">' + arrow('M4 12h15M13 6l6 6-6 6') + '</button></div>' +
      '<p class="lbx__cap"></p>';
    body.appendChild(lbx);
    var lImg = $('.lbx__img', lbx), lCap = $('.lbx__cap', lbx), lCount = $('.lbx__count', lbx), lStage = $('.lbx__stage', lbx);
    var lClose = $('.lbx__close', lbx), lPrev = $('.lbx__nav--prev', lbx), lNext = $('.lbx__nav--next', lbx);
    var group = [], idx = 0, lastFocus = null, isOpen = false;

    var sizesFor = function (a) {
      var w = +a.getAttribute('data-w') || 1, h = +a.getAttribute('data-h') || 1;
      var boxW = lStage.clientWidth - 2 * parseFloat(getComputedStyle(lStage).paddingLeft || 0), boxH = lStage.clientHeight;
      return Math.max(200, Math.ceil(Math.min(boxW, boxH * w / h))) + 'px';
    };
    var load = function (a, done) {
      var pre = new Image();
      pre.sizes = sizesFor(a);
      pre.srcset = a.getAttribute('data-srcset') || '';
      pre.src = a.href;
      if (done) { if (pre.decode) pre.decode().then(done, done); else pre.onload = pre.onerror = done; }
    };
    var show = function (i) {
      idx = (i + group.length) % group.length;
      var a = group[idx];
      lImg.classList.remove('is-ready');
      lCap.textContent = a.getAttribute('data-caption') || '';
      lCount.textContent = (idx + 1) + ' / ' + group.length;
      var many = group.length > 1;
      lPrev.hidden = lNext.hidden = !many;
      load(a, function () {
        if (group[idx] !== a) return;
        lImg.sizes = sizesFor(a);
        lImg.srcset = a.getAttribute('data-srcset') || '';
        lImg.src = a.href;
        lImg.alt = a.getAttribute('data-caption') || '';
        raf(function () { raf(function () { lImg.classList.add('is-ready'); }); });
        if (many) { load(group[(idx + 1) % group.length]); load(group[(idx - 1 + group.length) % group.length]); }
      });
    };
    var open = function (a) {
      group = lbItems.filter(function (x) { return x.getAttribute('data-lb') === a.getAttribute('data-lb') && !x.hidden; });
      lastFocus = doc.activeElement;
      isOpen = true;
      lbx.classList.add('is-open'); lbx.setAttribute('aria-hidden', 'false');
      body.classList.add('is-locked');
      show(Math.max(0, group.indexOf(a)));
      lClose.focus();
    };
    var close = function () {
      isOpen = false;
      lbx.classList.remove('is-open'); lbx.setAttribute('aria-hidden', 'true');
      body.classList.remove('is-locked');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    };
    doc.addEventListener('click', function (e) {
      var a = e.target.closest('a.lb');
      if (a) { e.preventDefault(); open(a); return; }
      var b = e.target.closest('[data-lb-open]');
      if (b) {
        var first = lbItems.filter(function (x) { return x.getAttribute('data-lb') === b.getAttribute('data-lb-open'); })[0];
        if (first) open(first);
      }
    });
    lClose.addEventListener('click', close);
    lPrev.addEventListener('click', function () { show(idx - 1); });
    lNext.addEventListener('click', function () { show(idx + 1); });
    lStage.addEventListener('click', function (e) { if (e.target === lStage) close(); });
    doc.addEventListener('keydown', function (e) {
      if (!isOpen) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(idx - 1);
      else if (e.key === 'ArrowRight') show(idx + 1);
      else if (e.key === 'Tab') {
        var f = [lClose, lPrev, lNext].filter(function (el) { return !el.hidden; }), i = f.indexOf(doc.activeElement);
        e.preventDefault();
        f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
      }
    });
    var tx = null, ty = null;
    lStage.addEventListener('touchstart', function (e) { if (e.touches.length === 1) { tx = e.touches[0].clientX; ty = e.touches[0].clientY; } else tx = null; }, { passive: true });
    lStage.addEventListener('touchend', function (e) {
      if (tx === null) return;
      var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty; tx = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.2) show(idx + (dx < 0 ? 1 : -1));
      else if (dy > 110 && Math.abs(dy) > Math.abs(dx) * 1.5) close();
    }, { passive: true });
  }

  /* -------------------------------------------------- gallery filters ---- */
  var filters = $('[data-filters]'), gal = $('[data-gallery]');
  if (filters && gal) {
    filters.addEventListener('click', function (e) {
      var b = e.target.closest('[data-filter]');
      if (!b || b.classList.contains('is-active')) return;
      var f = b.getAttribute('data-filter');
      $$('[data-filter]', filters).forEach(function (c) { var on = c === b; c.classList.toggle('is-active', on); c.setAttribute('aria-pressed', String(on)); });
      gal.classList.add('is-switching');
      setTimeout(function () {
        $$('.gallery__item', gal).forEach(function (it) { it.hidden = !(f === 'all' || it.getAttribute('data-cat') === f); });
        gal.classList.remove('is-switching');
      }, reduce ? 0 : 260);
    });
  }

  /* ----------------------------------------------- map, only on request ---- */
  $$('[data-map]').forEach(function (m) {
    var b = $('[data-map-load]', m);
    if (!b) return;
    b.addEventListener('click', function () {
      var f = doc.createElement('iframe');
      f.src = m.getAttribute('data-src');
      f.title = m.getAttribute('data-title') || 'Map';
      f.loading = 'lazy';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      f.setAttribute('allowfullscreen', '');
      m.appendChild(f);
      m.classList.add('is-loaded');
    });
  });

  /* ---------------------------------------------------- enquiry form ---- */
  var form = $('[data-enquiry]');
  if (form) {
    var lab = {};
    try { lab = JSON.parse(form.getAttribute('data-labels')); } catch (err) {}
    var el = form.elements, q = new URLSearchParams(location.search);
    ['room', 'in', 'out', 'guests'].forEach(function (k) { var v = q.get(k); if (v && el[k]) el[k].value = v; });
    var iso = function (d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); };
    el['in'].min = iso(new Date());
    el['in'].addEventListener('change', function () {
      if (!this.value) return;
      var p = this.value.split('-'), d = new Date(+p[0], +p[1] - 1, +p[2] + 1);
      el.out.min = iso(d);
      if (!el.out.value || el.out.value <= this.value) el.out.value = iso(d);
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = $('.form__error', form), name = el['name'].value.trim(), mail = el.email.value.trim();
      if (!name || !/^\S+@\S+\.\S+$/.test(mail)) {
        err.textContent = lab.required || ''; err.hidden = false;
        (name ? el.email : el['name']).focus();
        return;
      }
      err.hidden = true;
      var room = el.room.options[el.room.selectedIndex].text;
      var lines = [lab.name + ': ' + name, lab.email + ': ' + mail];
      if (el.phone.value.trim()) lines.push(lab.phone + ': ' + el.phone.value.trim());
      lines.push(lab.room + ': ' + room);
      if (el['in'].value) lines.push(lab['in'] + ': ' + el['in'].value);
      if (el.out.value) lines.push(lab.out + ': ' + el.out.value);
      lines.push(lab.guests + ': ' + el.guests.value);
      if (el.msg.value.trim()) lines.push('', lab.msg + ':', el.msg.value.trim());
      var subject = lab.subject + (el.room.value ? ' — ' + room : '') + (el['in'].value ? ' (' + el['in'].value + (el.out.value ? ' → ' + el.out.value : '') + ')' : '');
      location.href = 'mailto:' + form.getAttribute('data-to') + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      $('.form__done', form).hidden = false;
    });
  }
})();
