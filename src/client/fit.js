/*
 * Browser helper (classic script, no modules): keeps wide maths inside its column.
 * Used by tools/build-pdf.mjs before printing, and by the website (call again on resize).
 *
 *   <script src="assets/fit.js"></script>
 *   PT.fitMath(rootElement = document)   -> number of maths blocks that were adjusted
 *
 * For every display block (.math-fit, see src/rich.mjs):
 *   1. if it fits, leave it;
 *   2. else shrink its font-size to fit (down to MIN_SCALE);
 *   3. if that is not enough and a line-breakable version exists (.math-alt), show that instead;
 *   4. last resort: scale it with a transform so it can never overflow or be clipped.
 * Inline maths (.katex outside .math-fit) that is wider than its line box is shrunk the same way.
 */
(function () {
  var MIN_SCALE = 0.66;

  function reset(el) {
    el.style.fontSize = '';
    el.removeAttribute('data-fit');
    var inner = el.querySelector(':scope > .math-inner');
    var alt = el.querySelector(':scope > .math-alt');
    if (inner) {
      inner.hidden = false;
      inner.style.transform = '';
      inner.style.transformOrigin = '';
      inner.style.marginBottom = '';
    }
    if (alt) alt.hidden = true;
  }

  function natural(inner) {
    // .katex-display is block-level; measure the rendered formula itself.
    var html = inner.querySelector('.katex-html') || inner;
    return Math.max(html.scrollWidth, html.getBoundingClientRect().width);
  }

  function fitDisplay(el) {
    reset(el);
    var avail = el.clientWidth;
    var inner = el.querySelector(':scope > .math-inner');
    if (!inner || !avail) return false;
    var need = natural(inner);
    if (need <= avail + 0.5) return false;
    var scale = avail / need;
    if (scale >= MIN_SCALE) {
      el.style.fontSize = Math.floor(scale * 1000) / 10 + '%';
      // rounding can leave a hair of overflow
      var again = natural(inner);
      if (again > avail + 0.5) el.style.fontSize = Math.floor(scale * (avail / again) * 990) / 10 + '%';
      el.setAttribute('data-fit', 'scaled');
      return true;
    }
    var alt = el.querySelector(':scope > .math-alt');
    if (alt) {
      inner.hidden = true;
      alt.hidden = false;
      el.setAttribute('data-fit', 'wrapped');
      // a single unbreakable chunk may still be too wide
      var w = alt.scrollWidth;
      if (w > avail + 0.5) el.style.fontSize = Math.max(MIN_SCALE, avail / w) * 100 + '%';
      return true;
    }
    el.style.fontSize = MIN_SCALE * 100 + '%';
    var now = natural(inner);
    if (now > avail + 0.5) {
      var s = avail / now;
      var h = inner.getBoundingClientRect().height;
      inner.style.transformOrigin = '0 0';
      inner.style.transform = 'scale(' + s + ')';
      inner.style.marginBottom = -(h * (1 - s)) + 'px';
    }
    el.setAttribute('data-fit', 'forced');
    return true;
  }

  function fitInline(k) {
    k.style.fontSize = '';
    var box = k.parentElement;
    while (box && getComputedStyle(box).display.indexOf('inline') === 0) box = box.parentElement;
    if (!box) return false;
    var avail = box.clientWidth;
    var need = k.getBoundingClientRect().width;
    if (!avail || need <= avail + 0.5) return false;
    var cur = parseFloat(getComputedStyle(k).fontSize);
    k.style.fontSize = Math.max(cur * MIN_SCALE, (cur * avail) / need) * 0.99 + 'px';
    return true;
  }

  function fitMath(root) {
    root = root || document;
    var n = 0;
    var blocks = root.querySelectorAll('.math-fit');
    for (var i = 0; i < blocks.length; i++) if (fitDisplay(blocks[i])) n++;
    var inl = root.querySelectorAll('.katex');
    for (var j = 0; j < inl.length; j++) {
      if (inl[j].closest('.math-fit')) continue;
      if (fitInline(inl[j])) n++;
    }
    return n;
  }

  /** Report anything that still sticks out of its column (used by the PDF build as a check). */
  function findOverflow(root) {
    root = root || document;
    var out = [];
    var els = root.querySelectorAll('.math-fit, .katex, .fig, .q-box, .step-body, .answer-text');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var host = el.closest('.step-body, .q-box, .q-text, .answer, .sheet') || document.body;
      if (host === el) host = el.parentElement.closest('.step-body, .q-box, .answer, .sheet') || document.body;
      var a = el.getBoundingClientRect();
      var b = host.getBoundingClientRect();
      if (a.width && (a.right > b.right + 1 || a.left < b.left - 1)) {
        var q = el.closest('.q');
        out.push({ q: q ? q.id : '', cls: el.className && el.className.baseVal === undefined ? el.className : 'svg', over: Math.round(a.right - b.right) });
      }
    }
    return out;
  }

  var g = typeof window !== 'undefined' ? window : globalThis;
  g.PT = g.PT || {};
  g.PT.fitMath = fitMath;
  g.PT.findOverflow = findOverflow;
})();
