/*
 * Rich text, maths, marks and figures -> safe HTML strings (build time, no DOM).
 *
 * Exports
 *   escapeHtml(s)                     HTML-escape text (& < > " ').
 *   renderMath(tex, { display, wrap }) KaTeX -> HTML. Display maths is wrapped for fitting:
 *                                      <span class="math-fit math-display"><span class="math-inner">KaTeX</span>
 *                                      [<span class="math-alt" hidden>line-breakable KaTeX</span>]</span>
 *                                      `wrap: true` adds the line-breakable alternative for long one-line equations;
 *                                      src/client/fit.js swaps it in when scaling alone would make the maths too small.
 *   renderRich(s)                     contract "Rich text" -> HTML: $..$ inline maths, $$..$$ display maths,
 *                                      **bold** -> <strong>, everything else escaped.
 *   fmtMarks(n)                       0.5 -> "½", 1 -> "1", 1.5 -> "1½" (never "0.5").
 *   marksHtml(n)                      fmtMarks with the ½ wrapped in <span class="half"> (for hand-font marks).
 *   marksLabel(n)                     "½ mark", "1 mark", "4 marks".
 *   TYPE_LABELS, typeLabel(type)       "mcq" -> "MCQ", "assertion-reason" -> "Assertion-Reason", ...
 *   inlineFigure(contentDir, relPath, { cls, idPrefix, maxWidthMm, alt })
 *                                      reads an SVG and returns <figure class="fig {cls}"> with the SVG inlined,
 *                                      ids prefixed (so many figures can share one page), width capped.
 *
 * Class names produced here
 *   .math-fit .math-display .math-inner .math-alt   display maths wrapper (fit.js reads these)
 *   .fig .fig-missing                                figures
 */
import fs from 'node:fs';
import path from 'node:path';
import katex from 'katex';

const KATEX_OPTS = { throwOnError: false, strict: 'ignore', output: 'htmlAndMathml', trust: false };
const MATH = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;

export function escapeHtml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

const STRUCTURED = /\\begin\{(aligned|alignedat|gathered|bmatrix|pmatrix|vmatrix|Vmatrix|matrix|array|cases|split)\}|\\\\/;

/** KaTeX -> HTML. Display maths gets the fit wrapper. */
export function renderMath(tex, { display = false, wrap } = {}) {
  const src = String(tex ?? '').trim();
  if (!display) {
    return katex.renderToString(src, { ...KATEX_OPTS, displayMode: false });
  }
  const main = katex.renderToString(src, { ...KATEX_OPTS, displayMode: true });
  const wantAlt = wrap ?? (src.length > 38 && !STRUCTURED.test(src));
  const alt = wantAlt
    ? `<span class="math-alt" hidden>${katex.renderToString(`\\displaystyle ${src}`, { ...KATEX_OPTS, displayMode: false })}</span>`
    : '';
  return `<span class="math-fit math-display"><span class="math-inner">${main}</span>${alt}</span>`;
}

/** Contract rich text -> HTML. */
export function renderRich(s) {
  if (s === undefined || s === null || s === '') return '';
  const parts = [];
  // Replace maths with placeholders first so ** can span across maths and nothing inside maths is touched.
  const withHolders = String(s).replace(MATH, (_, disp, inl) => {
    parts.push(disp !== undefined ? renderMath(disp, { display: true }) : renderMath(inl, { display: false }));
    return `\u0001${parts.length - 1}\u0002`;
  });
  let html = escapeHtml(withHolders);
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\u0001(\d+)\u0002/g, (_, i) => parts[Number(i)]);
  return html;
}

/** 0.5 -> ½, 1.5 -> 1½, 2 -> 2. */
export function fmtMarks(n) {
  if (typeof n !== 'number' || !Number.isFinite(n)) return '';
  const whole = Math.floor(n);
  const half = Math.abs(n - whole - 0.5) < 1e-9;
  if (half) return whole ? `${whole}½` : '½';
  return String(n);
}

/** Like fmtMarks, but the ½ is wrapped in <span class="half"> so CSS can size it (hand fonts draw it small). */
export function marksHtml(n) {
  return escapeHtml(fmtMarks(n)).replace('½', '<span class="half">½</span>');
}

export function marksLabel(n) {
  return `${fmtMarks(n)} ${n === 1 || n === 0.5 ? 'mark' : 'marks'}`;
}

export const TYPE_LABELS = {
  mcq: 'MCQ',
  'assertion-reason': 'Assertion-Reason',
  short: 'Short answer',
  long: 'Long answer',
  case: 'Case study',
};
export const typeLabel = (t) => TYPE_LABELS[t] || String(t || '');

const PT_TO_PX = 96 / 72;
const PX_TO_MM = 25.4 / 96;

function svgNaturalPx(svg) {
  const num = (attr) => {
    const m = svg.match(new RegExp(`<svg[^>]*\\s${attr}="([\\d.]+)(pt|px|mm)?"`));
    if (!m) return null;
    const v = parseFloat(m[1]);
    if (m[2] === 'pt') return v * PT_TO_PX;
    if (m[2] === 'mm') return v / PX_TO_MM;
    return v;
  };
  let w = num('width');
  let h = num('height');
  const vb = svg.match(/<svg[^>]*\sviewBox="([^"]+)"/);
  if (vb) {
    const [, , vw, vh] = vb[1].trim().split(/[\s,]+/).map(Number);
    if (!w && !h) {
      w = vw;
      h = vh;
    } else if (w && !h) h = (w * vh) / vw;
    else if (h && !w) w = (h * vw) / vh;
  }
  return { w: w || 460, h: h || 300, hasViewBox: !!vb };
}

/**
 * Inline an SVG figure. Ids are prefixed so several matplotlib figures can share a page.
 * maxWidthMm caps the printed width; the figure never exceeds its container (max-width: 100%).
 */
export function inlineFigure(contentDir, relPath, { cls = '', idPrefix = 'f', maxWidthMm = 110, maxHeightMm = 95, alt = '' } = {}) {
  if (!relPath) return '';
  const file = path.join(contentDir, relPath);
  let svg;
  try {
    svg = fs.readFileSync(file, 'utf8');
  } catch {
    return `<figure class="fig fig-missing ${cls}"><figcaption>Figure not found: ${escapeHtml(relPath)}</figcaption></figure>`;
  }
  svg = svg
    .replace(/<\?xml[\s\S]*?\?>/g, '')
    .replace(/<!DOCTYPE[\s\S]*?>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<metadata[\s\S]*?<\/metadata>/gi, '')
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/\son[a-z]+="[^"]*"/gi, '')
    .trim();
  const { w, h, hasViewBox } = svgNaturalPx(svg);
  const pre = `${idPrefix}-`;
  svg = svg
    .replace(/\sid="([^"]+)"/g, (_, id) => ` id="${pre}${id}"`)
    .replace(/url\(#([^)]+)\)/g, (_, id) => `url(#${pre}${id})`)
    .replace(/(xlink:href|href)="#([^"]+)"/g, (_, a, id) => `${a}="#${pre}${id}"`);
  // Make the root SVG fluid: keep the viewBox, drop fixed width/height.
  svg = svg.replace(/<svg\b([^>]*)>/, (m, attrs) => {
    let a = attrs.replace(/\s(width|height)="[^"]*"/g, '');
    if (!hasViewBox) a += ` viewBox="0 0 ${w} ${h}"`;
    if (!/preserveAspectRatio=/.test(a)) a += ' preserveAspectRatio="xMidYMid meet"';
    return `<svg${a} role="img"${alt ? ` aria-label="${escapeHtml(alt)}"` : ''}>`;
  });
  const naturalMm = w * PX_TO_MM;
  const byHeight = (maxHeightMm * w) / h;
  const widthMm = Math.min(naturalMm, maxWidthMm, byHeight);
  return `<figure class="fig ${cls}" style="--fig-w:${widthMm.toFixed(1)}mm">${svg}</figure>`;
}
