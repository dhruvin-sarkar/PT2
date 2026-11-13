/*
 * Hand-drawn doodles for the website (build time, deterministic). Extends src/sketch.mjs:
 * every stroke is a slightly wobbly Catmull-Rom curve through jittered points, in currentColor.
 *
 * Exports
 *   chapterDoodle(chapter)     a 64x48 topic doodle for the chapter index card (fallback: a star)
 *   arrowDoodle(seed, dir)     curved pen arrow; dir "right" (80x32) or "down" (32x56)
 *   starDoodle(seed)           small five-point star
 *   pageDoodle(seed)           page with a folded corner (PDF links)
 *   pencilDoodle(seed)         pencil (brand mark)
 *   moonDoodle(seed), sunDoodle(seed)   theme toggle icons
 *   faviconSvg()               standalone SVG document for docs/assets/favicon.svg
 */
import { rng } from '../sketch.mjs';

const f = (n) => (Math.round(n * 10) / 10).toString();
const ATTR = 'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"';

/** Smooth curve through points (Catmull-Rom -> cubic Bezier). */
function smooth(pts) {
  let d = `M${f(pts[0][0])} ${f(pts[0][1])}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i];
    const p1 = pts[i];
    const p2 = pts[i + 1];
    const p3 = pts[i + 2] || p2;
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${f(c1[0])} ${f(c1[1])} ${f(c2[0])} ${f(c2[1])} ${f(p2[0])} ${f(p2[1])}`;
  }
  return d;
}

/** A pen stroke through the given points; interior points wobble by `a`. */
function stroke(r, pts, a = 0.7) {
  const j = pts.map(([x, y], i) => (i === 0 || i === pts.length - 1 ? [x + (r() - 0.5) * a * 0.6, y + (r() - 0.5) * a * 0.6] : [x + (r() - 0.5) * a, y + (r() - 0.5) * a]));
  return smooth(j);
}

/** Straight-ish line, subdivided so it bows a little. */
function line(r, x1, y1, x2, y2, a = 0.7, n = 3) {
  const pts = [];
  for (let i = 0; i <= n; i++) pts.push([x1 + ((x2 - x1) * i) / n, y1 + ((y2 - y1) * i) / n]);
  return stroke(r, pts, a);
}

/** Two short strokes forming an arrow head at (x, y) pointing along angle `ang` (radians). */
function head(r, x, y, ang, len = 4.2) {
  const a1 = ang + Math.PI - 0.5 + (r() - 0.5) * 0.15;
  const a2 = ang + Math.PI + 0.5 + (r() - 0.5) * 0.15;
  return `M${f(x + Math.cos(a1) * len)} ${f(y + Math.sin(a1) * len)} L${f(x)} ${f(y)} L${f(x + Math.cos(a2) * len)} ${f(y + Math.sin(a2) * len)}`;
}

function arrowLine(r, x1, y1, x2, y2, a = 0.6) {
  return `${line(r, x1, y1, x2, y2, a)} ${head(r, x2, y2, Math.atan2(y2 - y1, x2 - x1))}`;
}

function ellipse(r, cx, cy, rx, ry, n = 22, overlap = 0.3) {
  const start = -2 + r() * 0.5;
  const pts = [];
  for (let i = 0; i <= n; i++) {
    const t = start + ((Math.PI * 2 + overlap) * i) / n;
    const k = 1 + (r() - 0.5) * 0.06;
    pts.push([cx + Math.cos(t) * rx * k, cy + Math.sin(t) * ry * k]);
  }
  return stroke(r, pts, 0.3);
}

function sample(fn, t0, t1, n) {
  const pts = [];
  for (let i = 0; i <= n; i++) {
    const t = t0 + ((t1 - t0) * i) / n;
    pts.push(fn(t));
  }
  return pts;
}

const dot = (x, y, rad = 1.3) => `<circle cx="${f(x)}" cy="${f(y)}" r="${rad}" fill="currentColor" stroke="none"/>`;
const path = (d, extra = '') => `<path d="${d}" ${ATTR}${extra}/>`;

function svg(cls, vb, inner, sw = 1.6) {
  return `<svg class="${cls}" viewBox="${vb}" aria-hidden="true" focusable="false" stroke-width="${sw}">${inner}</svg>`;
}

/** Diagonal hatch lines clipped to a polygon (drawn by hand: short parallel strokes). */
function hatch(r, poly, gap = 4.2) {
  const xs = poly.map((p) => p[0]);
  const ys = poly.map((p) => p[1]);
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const out = [];
  // lines y = x + c, intersect with polygon edges
  for (let c = minY - maxX; c <= maxY - minX; c += gap) {
    const hits = [];
    for (let i = 0; i < poly.length; i++) {
      const [x1, y1] = poly[i];
      const [x2, y2] = poly[(i + 1) % poly.length];
      const dx = x2 - x1, dy = y2 - y1;
      const den = dy - dx;
      if (Math.abs(den) < 1e-9) continue;
      const t = (x1 + c - y1) / den;
      if (t >= 0 && t <= 1) hits.push(x1 + dx * t);
    }
    hits.sort((a, b) => a - b);
    for (let k = 0; k + 1 < hits.length; k += 2) {
      const xa = hits[k] + 0.8, xb = hits[k + 1] - 0.8;
      if (xb - xa > 1.5) out.push(line(r, xa, xa + c, xb, xb + c, 0.4, 1));
    }
  }
  return out.join(' ');
}

const DOODLES = {
  // Relations and functions: arrow diagram between two sets
  1: (r) => {
    const L = [[16, 14], [16, 24], [16, 34]];
    const R = [[48, 17], [48, 31]];
    return [
      path(ellipse(r, 16, 24, 9, 18)),
      path(ellipse(r, 48, 24, 9, 18)),
      ...L.map(([x, y]) => dot(x, y)),
      ...R.map(([x, y]) => dot(x, y)),
      path(arrowLine(r, 18.5, 14, 45, 17)),
      path(arrowLine(r, 18.5, 24, 45, 18.5)),
      path(arrowLine(r, 18.5, 34, 45, 31)),
    ].join('');
  },
  // Inverse trigonometric functions: the arcsin curve on axes
  2: (r) => {
    const curve = sample((t) => [32 + t * 18, 24 - (Math.asin(t) / (Math.PI / 2)) * 17], -1, 1, 14);
    return [path(arrowLine(r, 6, 24, 60, 24)), path(arrowLine(r, 32, 45, 32, 3)), path(stroke(r, curve, 0.5), ' stroke-width="2"'), dot(50, 7), dot(14, 41)].join('');
  },
  // Matrices: square brackets around a grid of entries
  3: (r) => {
    const br = (x, s) => stroke(r, [[x + 4 * s, 6], [x, 6], [x, 24], [x, 42], [x + 4 * s, 42]], 0.5);
    const cells = [];
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) cells.push(path(line(r, 18 + j * 11, 13 + i * 11, 22 + j * 11, 13 + i * 11, 0.6, 1), ' stroke-width="2.2"'));
    return [path(br(12, 1)), path(br(52, -1)), ...cells].join('');
  },
  // Determinants: vertical bars and the cross-multiplication diagonals
  4: (r) => [
    path(line(r, 14, 6, 14, 42, 0.8)),
    path(line(r, 50, 6, 50, 42, 0.8)),
    `<text x="20" y="20" class="dd-t">a</text><text x="37" y="20" class="dd-t">b</text><text x="20" y="38" class="dd-t">c</text><text x="37" y="38" class="dd-t">d</text>`,
    path(line(r, 21, 12, 42, 35, 0.9), ' stroke-dasharray="2.5 2.5" stroke-width="1.2"'),
    path(line(r, 42, 12, 21, 35, 0.9), ' stroke-dasharray="2.5 2.5" stroke-width="1.2"'),
  ].join(''),
  // Continuity and differentiability: smooth curve with a tangent at a point
  5: (r) => {
    const fx = (x) => 30 - 12 * Math.sin((x - 6) / 9);
    const curve = sample((x) => [x, fx(x)], 4, 60, 16);
    const x0 = 26, y0 = fx(x0), m = (-12 / 9) * Math.cos((x0 - 6) / 9);
    return [path(stroke(r, curve, 0.5), ' stroke-width="2"'), path(line(r, x0 - 16, y0 - 16 * m, x0 + 16, y0 + 16 * m, 0.6)), dot(x0, y0, 1.8)].join('');
  },
  // Application of derivatives: a hill with a horizontal tangent at the maximum
  6: (r) => {
    const curve = sample((x) => [x, 40 - 26 * Math.exp(-(((x - 32) / 13) ** 2))], 4, 60, 16);
    return [path(stroke(r, curve, 0.5), ' stroke-width="2"'), path(line(r, 20, 14, 44, 14, 0.5)), dot(32, 14, 1.8), path(line(r, 32, 17, 32, 41, 0.4), ' stroke-dasharray="2 2.5" stroke-width="1.1"'), path(line(r, 4, 42, 60, 42, 0.6))].join('');
  },
  // Integrals: the integral sign with limits
  7: (r) => {
    const s = [[34, 6], [30, 4.5], [27, 8], [26, 16], [25, 26], [24, 36], [21, 43], [17, 42.5]];
    return [path(stroke(r, s, 0.4), ' stroke-width="2.2"'), `<text x="36" y="12" class="dd-t dd-s">b</text><text x="14" y="47" class="dd-t dd-s">a</text><text x="34" y="31" class="dd-t">dx</text>`].join('');
  },
  // Application of integrals: shaded area under a curve
  8: (r) => {
    const fx = (x) => 40 - 22 * Math.sqrt((x - 6) / 50);
    const curve = sample((x) => [x, fx(x)], 6, 58, 12);
    const poly = [[20, 40], ...sample((x) => [x, fx(x)], 20, 46, 6), [46, 40]];
    return [path(arrowLine(r, 4, 40, 61, 40)), path(arrowLine(r, 6, 46, 6, 3)), path(stroke(r, curve, 0.4), ' stroke-width="2"'), path(hatch(r, poly, 3.6), ' stroke-width="1.1"'), path(line(r, 20, 40, 20, fx(20), 0.3, 1)), path(line(r, 46, 40, 46, fx(46), 0.3, 1))].join('');
  },
  // Differential equations: a slope field with one solution curve
  9: (r) => {
    const segs = [];
    for (let i = 0; i < 4; i++) {
      for (let j = 0; j < 5; j++) {
        const x = 9 + j * 11.5, y = 8 + i * 11;
        const slope = (x - 32) / 26 - (y - 24) / 40;
        const a = Math.atan(slope);
        segs.push(path(line(r, x - Math.cos(a) * 3.4, y - Math.sin(a) * 3.4, x + Math.cos(a) * 3.4, y + Math.sin(a) * 3.4, 0.25, 1), ' stroke-width="1.2"'));
      }
    }
    const curve = sample((x) => [x, 30 - ((x - 32) ** 2) / 70 + 2], 4, 60, 12);
    return [...segs, path(stroke(r, curve, 0.4), ' stroke-width="2"')].join('');
  },
  // Vector algebra: triangle law of addition
  10: (r) => [
    path(arrowLine(r, 8, 40, 34, 30)),
    path(arrowLine(r, 34, 30, 54, 8)),
    path(arrowLine(r, 8, 40, 54, 8), ' stroke-width="2"'),
    `<text x="18" y="32" class="dd-t dd-s">a</text><text x="47" y="25" class="dd-t dd-s">b</text>`,
  ].join(''),
  // Three dimensional geometry: axes and a line through a point
  11: (r) => [
    path(arrowLine(r, 26, 30, 26, 3)),
    path(arrowLine(r, 26, 30, 60, 30)),
    path(arrowLine(r, 26, 30, 8, 46)),
    path(line(r, 6, 14, 58, 44, 0.6), ' stroke-dasharray="3 2.5" stroke-width="1.2"'),
    dot(40, 34.4, 1.9),
    `<text x="28" y="8" class="dd-t dd-s">z</text><text x="56" y="27" class="dd-t dd-s">y</text><text x="4" y="42" class="dd-t dd-s">x</text>`,
  ].join(''),
  // Linear programming: two constraints and the hatched feasible region
  12: (r) => {
    const poly = [[8, 42], [8, 18], [26, 26], [44, 42]];
    return [
      path(arrowLine(r, 6, 42, 61, 42)),
      path(arrowLine(r, 8, 46, 8, 3)),
      path(line(r, 8, 18, 50, 36.7, 0.5)),
      path(line(r, 18, 10, 46, 44, 0.5)),
      path(hatch(r, poly, 3.8), ' stroke-width="1.1"'),
      dot(26, 26, 1.9),
    ].join('');
  },
  // Probability: a two-stage tree diagram
  13: (r) => {
    const root = [8, 24];
    const mid = [[28, 12], [28, 36]];
    const leaves = [[52, 6], [52, 18], [52, 30], [52, 42]];
    return [
      dot(...root, 1.7),
      ...mid.map((m) => path(line(r, root[0] + 1.5, root[1], m[0] - 1.5, m[1], 0.5, 2)) + dot(...m, 1.6)),
      ...leaves.map((l, i) => path(line(r, mid[i >> 1][0] + 1.5, mid[i >> 1][1], l[0] - 1.5, l[1], 0.5, 2)) + dot(...l, 1.4)),
      `<text x="14" y="13" class="dd-t dd-s">p</text><text x="13" y="41" class="dd-t dd-s">q</text>`,
    ].join('');
  },
};

export function starDoodle(seed = 1, cls = 'doodle doodle-star') {
  const r = rng(seed + 404);
  const pts = [];
  for (let i = 0; i <= 10; i++) {
    const a = -Math.PI / 2 + (i * Math.PI * 4) / 5;
    pts.push([12 + Math.cos(a) * 9.5, 12.5 + Math.sin(a) * 9.5]);
  }
  return svg(cls, '0 0 24 24', path(pts.map(([x, y], i) => `${i ? 'L' : 'M'}${f(x + (r() - 0.5))} ${f(y + (r() - 0.5))}`).join(' ')), 1.5);
}

export function chapterDoodle(chapter) {
  const make = DOODLES[Number(chapter)];
  if (!make) return starDoodle(Number(chapter) || 1, 'doodle doodle-topic');
  return svg('doodle doodle-topic', '0 0 64 48', make(rng(Number(chapter) * 31 + 7)));
}

export function arrowDoodle(seed = 1, dir = 'right') {
  const r = rng(seed + 505);
  if (dir === 'down') {
    const pts = [[14, 3], [19, 16], [15, 30], [17, 44], [16, 51]];
    return svg('doodle doodle-arrow doodle-arrow-down', '0 0 32 56', path(stroke(r, pts, 1) + ' ' + head(r, 16, 52, Math.PI / 2 + 0.08, 6)));
  }
  const pts = [[3, 20], [20, 10], [42, 9], [62, 15], [74, 18]];
  return svg('doodle doodle-arrow', '0 0 80 32', path(stroke(r, pts, 1.2) + ' ' + head(r, 75, 18.5, 0.25, 6.5)));
}

export function pageDoodle(seed = 1) {
  const r = rng(seed + 606);
  const outline = stroke(r, [[5, 3], [13, 3], [19, 9], [19, 23], [5, 23], [5, 3]], 0.5);
  const fold = stroke(r, [[13, 3], [13, 9], [19, 9]], 0.3);
  const lines = [13, 17].map((y) => line(r, 8.5, y, 15.5, y, 0.3, 1)).join(' ');
  return svg('doodle doodle-page', '0 0 24 26', path(`${outline} ${fold} ${lines}`), 1.5);
}

export function pencilDoodle(seed = 1) {
  const r = rng(seed + 707);
  const body = stroke(r, [[6, 22], [21, 7], [25, 11], [10, 26], [5, 27], [6, 22]], 0.4);
  const tip = line(r, 6, 22, 10, 26, 0.2, 1);
  const band = line(r, 18.5, 9.5, 22.5, 13.5, 0.3, 1);
  return svg('doodle doodle-pencil', '0 0 30 30', path(`${body} ${tip} ${band}`), 1.6);
}

export function moonDoodle(seed = 1) {
  const r = rng(seed + 808);
  // crescent: the outer circle's long arc, closed by the inner circle's arc between the same two tips
  const c1 = [11.5, 12.5], r1 = 8.5, c2 = [16, 8.5], r2 = 7;
  const dx = c2[0] - c1[0], dy = c2[1] - c1[1], d = Math.hypot(dx, dy);
  const a = (r1 * r1 - r2 * r2 + d * d) / (2 * d), h = Math.sqrt(r1 * r1 - a * a);
  const mx = c1[0] + (a * dx) / d, my = c1[1] + (a * dy) / d;
  const p1 = [mx + (h * dy) / d, my - (h * dx) / d], p2 = [mx - (h * dy) / d, my + (h * dx) / d];
  const ang = (c, p) => Math.atan2(p[1] - c[1], p[0] - c[0]);
  let a1 = ang(c1, p1), a2 = ang(c1, p2);
  if (a2 < a1) a2 += Math.PI * 2;
  const away = Math.atan2(-dy, -dx);
  const inSpan = (x, s, e) => { while (x < s) x += Math.PI * 2; return x <= e; };
  if (!inSpan(away, a1, a2)) [a1, a2] = [a2, a1 + Math.PI * 2];
  const outer = sample((t) => [c1[0] + Math.cos(t) * r1, c1[1] + Math.sin(t) * r1], a1, a2, 16);
  let b1 = ang(c2, outer[outer.length - 1]), b2 = ang(c2, outer[0]);
  const toward = Math.atan2(-dy, -dx);
  let s = b1, e = b2;
  if (e < s) e += Math.PI * 2;
  if (!inSpan(toward, s, e)) e -= Math.PI * 2;
  const inner = sample((t) => [c2[0] + Math.cos(t) * r2, c2[1] + Math.sin(t) * r2], s, e, 10);
  return svg('doodle doodle-moon', '0 0 24 24', path(`${stroke(r, outer, 0.3)} ${stroke(r, inner, 0.25).replace(/^M/, 'L')}`), 1.6);
}

/**
 * Wobbly box drawn twice round, like a pen outline, stretched to fill its positioned parent.
 * w/h should be close to the box's real size in px so the wobble reads as handwriting, not distortion.
 */
export function roughBox(seed = 1, { w = 160, h = 44, wobble = 1.6, cls = 'sk sk-box sk-rough' } = {}) {
  const r = rng(seed + 1313);
  const pad = 3;
  const L = pad, T = pad, R = w - pad, B = h - pad;
  const passes = [];
  for (let p = 0; p < 2; p++) {
    const j = (v, k = 1) => v + (r() - 0.5) * wobble * 2 * k;
    const o = () => 1.5 + r() * (p ? 3 : 5);
    const side = (x1, y1, x2, y2) => line(r, x1, y1, x2, y2, wobble * 0.9, 2);
    const t = side(j(L) - o(), j(T), j(R) + o(), j(T));
    const rr = side(j(R), j(T) - o() * 0.4, j(R), j(B) + o() * 0.4);
    const b = side(j(R) + o(), j(B), j(L) - o(), j(B));
    const l = side(j(L), j(B) + o() * 0.4, j(L), j(T) - o() * 0.4);
    passes.push([t, rr, b, l].join(' '));
  }
  const ATTR_NS = `${ATTR} vector-effect="non-scaling-stroke"`;
  return `<svg class="${cls}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="${passes[0]}" ${ATTR_NS}/><path class="sk-pass2" d="${passes[1]}" ${ATTR_NS}/></svg>`;
}

/** A highlighter swipe: filled shape with ragged ends, stretched behind a label (fill: currentColor). */
export function swipe(seed = 1, cls = 'swipe') {
  const r = rng(seed + 1717);
  const j = (v, a) => v + (r() - 0.5) * a;
  const top = [[6, j(9, 3)], [60, j(8, 3)], [120, j(9, 3)], [174, j(7, 3)], [195, j(8, 2)]];
  const right = [[j(199, 2), 14], [j(196, 2), 21], [j(199, 2), 28]];
  const bot = [[194, j(33, 2)], [140, j(34, 3)], [80, j(33, 3)], [20, j(35, 3)], [4, j(34, 2)]];
  const left = [[j(1, 2), 27], [j(4, 2), 20], [j(1, 2), 13]];
  const pts = [...top, ...right, ...bot, ...left];
  const d = `M${pts.map(([x, y]) => `${f(x)} ${f(y)}`).join(' L')} Z`;
  return `<svg class="${cls}" viewBox="0 0 200 42" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="${d}" fill="currentColor"/></svg>`;
}

export function sunDoodle(seed = 1) {
  const r = rng(seed + 909);
  const rays = [];
  for (let i = 0; i < 8; i++) {
    const a = (i * Math.PI) / 4 + 0.15;
    rays.push(line(r, 12 + Math.cos(a) * 7.5, 12 + Math.sin(a) * 7.5, 12 + Math.cos(a) * 10.8, 12 + Math.sin(a) * 10.8, 0.2, 1));
  }
  return svg('doodle doodle-sun', '0 0 24 24', path(`${ellipse(r, 12, 12, 4.6, 4.6, 14, 0.2)} ${rays.join(' ')}`), 1.6);
}

export function faviconSvg() {
  const r = rng(77);
  const circle = ellipse(r, 16, 16, 12.5, 12.5, 24, 0.45);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#fcfbf7"/><path d="${circle}" fill="none" stroke="#c22f2f" stroke-width="2.2" stroke-linecap="round"/><path d="${stroke(r, [[9.5, 16.5], [13, 21], [22.5, 10]], 0.4)}" fill="none" stroke="#24467f" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}
