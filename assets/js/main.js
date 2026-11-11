/* ProfitMaps AI site — interactions (no dependencies) */
(function () {
  'use strict';
  var doc = document;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }
  };

  /* Original seller images: if a hosted image cannot load, show a branded tile instead of a broken icon */
  function markFallback(img) {
    var box = img.closest('.pimg');
    if (box) box.classList.add('fb');
    var fig = img.closest('.shot-fig');
    if (fig) fig.style.display = 'none';
  }
  doc.querySelectorAll('img[data-orig]').forEach(function (img) {
    if (img.complete && img.naturalWidth === 0) markFallback(img);
    img.addEventListener('error', function () { markFallback(img); });
  });

  /* Mobile navigation */
  var menuBtn = doc.querySelector('.menu-btn');
  var links = doc.getElementById('nav-links');
  if (menuBtn && links) {
    menuBtn.addEventListener('click', function () {
      var open = menuBtn.getAttribute('aria-expanded') === 'true';
      menuBtn.setAttribute('aria-expanded', String(!open));
      links.classList.toggle('open', !open);
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { menuBtn.setAttribute('aria-expanded', 'false'); links.classList.remove('open'); }
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('open')) { menuBtn.setAttribute('aria-expanded', 'false'); links.classList.remove('open'); menuBtn.focus(); }
    });
  }

  /* FAQ accordion + search */
  doc.querySelectorAll('.faq-q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      doc.getElementById(btn.getAttribute('aria-controls')).hidden = open;
    });
  });
  var search = doc.querySelector('.faq-search');
  if (search) {
    var empty = doc.querySelector('.faq-empty');
    search.addEventListener('input', function () {
      var q = search.value.trim().toLowerCase(), shown = 0;
      doc.querySelectorAll('.faq-item').forEach(function (it) {
        var hit = !q || it.textContent.toLowerCase().indexOf(q) > -1;
        it.style.display = hit ? '' : 'none';
        if (hit) shown++;
      });
      if (empty) empty.style.display = shown ? 'none' : 'block';
    });
  }

  /* Scroll reveal */
  var rev = doc.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rev.forEach(function (el) { io.observe(el); });
  } else { rev.forEach(function (el) { el.classList.add('in'); }); }

  /* Pointer tilt on the hero product image */
  if (!reduce && window.matchMedia('(pointer:fine)').matches) {
    doc.querySelectorAll('[data-tilt]').forEach(function (stage) {
      var t = stage.querySelector('.tilt');
      if (!t) return;
      stage.addEventListener('pointermove', function (e) {
        var r = stage.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        t.style.transform = 'rotateY(' + (x * 16).toFixed(2) + 'deg) rotateX(' + (-y * 12).toFixed(2) + 'deg)';
      });
      stage.addEventListener('pointerleave', function () { t.style.transform = ''; });
    });
  }

  /* ---------- Centered promotional modal (24h cooldown) ---------- */
  var MODAL_KEY = 'pm_modal_dismissed_at';
  var overlay = doc.getElementById('pm-overlay');
  var modalOpen = false, lastFocus = null;
  function modalDue() {
    var t = parseInt(store.get(MODAL_KEY) || '0', 10);
    return !t || Date.now() - t > 24 * 60 * 60 * 1000;
  }
  function focusables() { return overlay.querySelectorAll('a[href],button:not([disabled])'); }
  function openModal() {
    if (!overlay || modalOpen) return;
    hideToast(true);
    modalOpen = true; lastFocus = doc.activeElement;
    overlay.hidden = false;
    requestAnimationFrame(function () { overlay.classList.add('show'); });
    doc.body.classList.add('modal-open');
    store.set(MODAL_KEY, String(Date.now()));
    setTimeout(function () { var c = overlay.querySelector('.pm-close'); if (c) c.focus(); }, 60);
  }
  function closeModal() {
    if (!modalOpen) return;
    modalOpen = false;
    overlay.classList.remove('show');
    doc.body.classList.remove('modal-open');
    setTimeout(function () { overlay.hidden = true; }, reduce ? 0 : 320);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
    scheduleToast(6000);
  }
  if (overlay) {
    overlay.querySelector('.pm-close').addEventListener('click', closeModal);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
    overlay.querySelectorAll('[data-close-after]').forEach(function (a) { a.addEventListener('click', function () { setTimeout(closeModal, 50); }); });
    doc.addEventListener('keydown', function (e) {
      if (!modalOpen) return;
      if (e.key === 'Escape') { e.preventDefault(); closeModal(); }
      if (e.key === 'Tab') {
        var f = focusables(), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  /* ---------- Bottom-left informational toast (no fake purchase activity) ---------- */
  var toast = doc.getElementById('pm-toast');
  var msgs = [];
  try { msgs = JSON.parse(toast.getAttribute('data-messages')); } catch (e) { msgs = []; }
  var idx = 0, toastTimer = null, hideTimer = null, toastStopped = false;
  function hideToast(silent) {
    if (!toast) return;
    toast.classList.remove('show');
    clearTimeout(hideTimer);
    if (silent) clearTimeout(toastTimer);
  }
  function showToast() {
    if (!toast || toastStopped || !msgs.length) return;
    if (modalOpen || doc.hidden) { scheduleToast(4000); return; }
    var m = msgs[idx++ % msgs.length];
    toast.querySelector('strong').textContent = m.t;
    toast.querySelector('span').textContent = m.d;
    var a = toast.querySelector('a');
    a.textContent = m.l; a.setAttribute('href', m.h);
    toast.classList.add('show');
    hideTimer = setTimeout(function () { toast.classList.remove('show'); scheduleToast(18000 + Math.random() * 8000); }, 6000);
  }
  function scheduleToast(ms) { clearTimeout(toastTimer); toastTimer = setTimeout(showToast, ms); }
  if (toast) {
    toast.querySelector('.toast-x').addEventListener('click', function () {
      hideToast(true);
      scheduleToast(22000);
    });
  }

  function start() {
    if (overlay && modalDue()) {
      setTimeout(openModal, 6500);           /* modal first; toast begins after it closes */
    } else {
      scheduleToast(5000);
    }
  }
  if (doc.readyState === 'complete') start(); else window.addEventListener('load', start);

  /* Footer year */
  var y = doc.getElementById('yr'); if (y) y.textContent = new Date().getFullYear();
})();
