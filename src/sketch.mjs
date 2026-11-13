/*
 * Hand-drawn notebook accents as small inline SVGs (deterministic: same seed -> same wobble).
 * All strokes use currentColor, so CSS decides the ink colour.
 *
 * Exports
 *   sketchBox(seed, { w, h })   wobbly rectangle with slightly overshooting corners, stretched to fill
 *                               its positioned parent: <svg class="sk sk-box" ...>. Parent needs position: relative.
 *   sketchCircle(seed)          a pen circle that does not quite close (question badge, correct option ring):
 *                               <svg class="sk sk-circle" ...>
 *   sketchTick(seed)            examiner's tick: <svg class="sk sk-tick" ...>
 *   sketchUnderline(seed)       loose underline stroke under a heading: <svg class="sk sk-underline" ...>
 *   rng(seed)                   the seeded PRNG used by all of the above.
 *
 * Every SVG is aria-hidden and uses vector-effect: non-scaling-stroke so the line weight stays even when the
 * shape is stretched.
 */

export function rng(seed) {
  let a = (Number(seed) * 2654435761) >>> 0 || 0x9e3779b9;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const f = (n) => (Math.round(n * 10) / 10).toString();
const STROKE = 'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"';

/** One slightly bowed line from (x1,y1) to (x2,y2). */
function bowed(r, x1, y1, x2, y2, bow) {
  const mx = (x1 + x2) / 2 + (r() - 0.5) * bow;
  const my = (y1 + y2) / 2 + (r() - 0.5) * bow;
  return `M${f(x1)} ${f(y1)} Q${f(mx)} ${f(my)} ${f(x2)} ${f(y2)}`;
}

export function sketchBox(seed = 1, { w = 600, h = 44, wobble = 2.2, overshoot = 5 } = {}) {
  const r = rng(seed);
  const j = (v) => v + (r() - 0.5) * wobble;
  const pad = 3;
  const L = pad, T = pad, R = w - pad, B = h - pad;
  const o = () => overshoot * (0.4 + r() * 0.8);
  const d = [
    bowed(r, j(L) - o(), j(T), j(R) + o(), j(T), wobble * 1.6),
    bowed(r, j(R), j(T) - o() * 0.5, j(R), j(B) + o() * 0.5, wobble * 1.2),
    bowed(r, j(R) + o(), j(B), j(L) - o(), j(B), wobble * 1.6),
    bowed(r, j(L), j(B) + o() * 0.5, j(L), j(T) - o() * 0.5, wobble * 1.2),
  ].join(' ');
  return `<svg class="sk sk-box" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="${d}" ${STROKE}/></svg>`;
}

export function sketchCircle(seed = 1, { size = 40 } = {}) {
  const r = rng(seed + 101);
  const c = size / 2;
  const rad = size / 2 - 3;
  const start = -2.2 + r() * 0.6; // radians, upper left
  const sweep = Math.PI * 2 + 0.35 + r() * 0.3; // overlaps its own start a little
  const n = 28;
  let d = '';
  for (let i = 0; i <= n; i++) {
    const t = start + (sweep * i) / n;
    const k = rad * (1 + (r() - 0.5) * 0.05) * (1 - 0.06 * (i / n));
    const x = c + Math.cos(t) * k * 1.04;
    const y = c + Math.sin(t) * k * 0.96;
    d += `${i ? 'L' : 'M'}${f(x)} ${f(y)} `;
  }
  return `<svg class="sk sk-circle" viewBox="0 0 ${size} ${size}" aria-hidden="true" focusable="false"><path d="${d.trim()}" ${STROKE}/></svg>`;
}

export function sketchTick(seed = 1) {
  const r = rng(seed + 202);
  const j = (v, a = 1.2) => v + (r() - 0.5) * a;
  const d = `M${f(j(2))} ${f(j(9))} Q${f(j(4.5))} ${f(j(11.5))} ${f(j(6))} ${f(j(14))} Q${f(j(10))} ${f(j(6))} ${f(j(17))} ${f(j(1.5))}`;
  return `<svg class="sk sk-tick" viewBox="0 0 19 16" aria-hidden="true" focusable="false"><path d="${d}" ${STROKE}/></svg>`;
}

export function sketchUnderline(seed = 1, { w = 300, h = 10 } = {}) {
  const r = rng(seed + 303);
  const y0 = h * 0.55;
  const pts = 6;
  let d = `M2 ${f(y0 + (r() - 0.5) * 2)}`;
  for (let i = 1; i <= pts; i++) {
    const x = 2 + ((w - 4) * i) / pts;
    const cx = x - (w - 4) / pts / 2;
    d += ` Q${f(cx)} ${f(y0 + (r() - 0.5) * 4)} ${f(x)} ${f(y0 + (r() - 0.5) * 2.4)}`;
  }
  return `<svg class="sk sk-underline" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="${d}" ${STROKE}/></svg>`;
}
