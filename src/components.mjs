/*
 * Question and solution HTML components, shared by the PDF sheets and the website.
 * Pure functions: content objects in, HTML strings out. Styles: src/styles/sheet.css.
 *
 * Exports
 *   renderQuestion(q, ctx)        the question card only (badge, type, marks, tinted box with text / figure /
 *                                 options / parts). ctx.reveal = true marks the correct option.
 *   renderSolution(q, ctx)        the solution only (concept line, solution figure, step grid or solved parts,
 *                                 answer strip, "Watch out" note).
 *   renderSolvedQuestion(q, ctx)  <article class="q q-solved"> = question (correct option marked) + solution.
 *   renderSteps(steps, ctx)       the three-column step grid on its own.
 *   renderAnswer(html, ctx)       the boxed "Answer" strip on its own.
 *   renderLevelHead(level, ctx)   level heading with its marks.
 *   correctOptionIndex(q)         0-3 from solution.answer "(B) ...", or -1.
 *   optionWidth(richText)         rough printed width of an option in body characters (picks the option layout).
 *   questionAnchor(q)             "q3" (used as the element id).
 *
 * ctx: { dir: content directory of the file (for figures), chapter, set, reveal, showPartText, idBase }
 *
 * Class names (all scoped by the block they sit in)
 *   article.q[data-type][id=q{n}]           one question; .q-solved when the solution follows
 *     header.q-head                          .q-badge (.sk-circle + .q-num) | .q-type | .q-source | .q-marks
 *     div.q-box                              lightly tinted restatement of the question
 *       div.q-text                           question rich text
 *       figure.fig.q-fig                     question figure (inline SVG)
 *       ol.q-options(.is-grid)(.is-row)      li.q-opt(.is-correct) > span.q-opt-letter (+ .sk-circle when correct)
 *                                              + span.q-opt-text. .is-grid = 2 x 2; .is-grid.is-row = all four
 *                                              on one line (short options); neither = one per line.
 *       ol.q-parts                           li.q-part(.is-alt) > .q-part-label .q-part-text .q-part-marks;
 *                                              li.q-or ("OR") sits before an alt part
 *   section.sol                              the solution
 *     p.sol-concept > span.sol-label         "Formula / idea" line
 *     figure.fig.sol-fig                     figure for the whole solution
 *     ol.steps > li.step                     grid row: span.step-n | div.step-body | span.step-marks(.has-marks)
 *       div.step-body > p.step-do, div.step-math (.math-fit), p.step-why, figure.fig.step-fig
 *       span.step-marks > .sk-tick + span.step-mark
 *     div.sol-part(.is-alt)                  one solved part: div.sol-or ("OR") when alt, h4.sol-part-head
 *                                              (.sol-part-label .sol-part-text .sol-part-marks), ol.steps, .answer
 *     div.answer(.answer-part)               boxed strip: .sk-box + span.answer-label + span.answer-text
 *     p.watch > span.watch-label             "Watch out" note
 *   section.level > h2.level-head            .level-name + .sk-underline + .level-marks
 */
import { renderRich, renderMath, escapeHtml, marksHtml, marksLabel, typeLabel, inlineFigure } from './rich.mjs';
import { sketchBox, sketchCircle, sketchTick, sketchUnderline } from './sketch.mjs';

const LETTERS = ['A', 'B', 'C', 'D'];

export const questionAnchor = (q) => `q${q.n}`;

export function correctOptionIndex(q) {
  const a = String(q?.solution?.answer ?? '');
  const m = a.match(/^\s*\(?\s*([A-Da-d])\s*\)/);
  return m ? LETTERS.indexOf(m[1].toUpperCase()) : -1;
}

const seedOf = (ctx, q, k = 0) => (Number(ctx?.chapter) || 0) * 1000 + (Number(q?.n) || 0) * 17 + k;
const figId = (ctx, q, k) => `${ctx?.idBase || 'c'}${ctx?.chapter ?? ''}q${q.n}${k}`;

/* ---- option layout: estimate how wide each option prints, in body-text character widths ---- */
const ZERO_WIDTH = new Set(['left', 'right', 'big', 'Big', 'bigg', 'Bigg', 'displaystyle', 'textstyle', 'limits', 'nolimits',
  'mathrm', 'mathbf', 'mathit', 'mathbb', 'mathcal', 'boldsymbol', 'text', 'textbf', 'operatorname', 'hat', 'vec', 'bar',
  'overline', 'overrightarrow', 'widehat', 'tilde', 'dot', 'ddot', 'mathsf']);
const WORD_OPS = new Set(['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'cosec', 'log', 'ln', 'exp', 'lim', 'max', 'min', 'det', 'adj']);
const WIDE_OPS = new Set(['le', 'ge', 'leq', 'geq', 'ne', 'neq', 'to', 'in', 'notin', 'subset', 'subseteq', 'cup', 'cap', 'times',
  'cdot', 'pm', 'mp', 'Rightarrow', 'Leftarrow', 'implies', 'iff', 'rightarrow', 'leftarrow', 'approx', 'equiv', 'perp', 'parallel']);

function braceGroup(s, i) {
  while (s[i] === ' ') i++;
  if (s[i] !== '{') {
    const m = s.slice(i).match(/^\\[a-zA-Z]+|^./s);
    return m ? [m[0], i + m[0].length] : ['', i];
  }
  let depth = 0;
  for (let j = i; j < s.length; j++) {
    if (s[j] === '{') depth++;
    else if (s[j] === '}' && --depth === 0) return [s.slice(i + 1, j), j + 1];
  }
  return [s.slice(i + 1), s.length];
}

function mathUnits(tex) {
  const s = String(tex);
  let u = 0;
  let i = 0;
  while (i < s.length) {
    const c = s[i];
    if (c === '\\') {
      const m = s.slice(i).match(/^\\([a-zA-Z]+|.)/s);
      const name = m[1];
      i += m[0].length;
      if (/^[dtc]?frac$|^binom$/.test(name)) {
        const [a, j] = braceGroup(s, i);
        const [b, k] = braceGroup(s, j);
        u += Math.max(mathUnits(a), mathUnits(b)) + 0.6;
        i = k;
      } else if (name === 'begin') {
        const [env, j] = braceGroup(s, i);
        const end = s.indexOf(`\\end{${env}}`, j);
        const body = s.slice(j, end < 0 ? s.length : end);
        const rows = body.split('\\\\').map((r) => r.split('&'));
        const cols = Math.max(...rows.map((r) => r.length));
        const colW = Array.from({ length: cols }, (_, ci) => Math.max(...rows.map((r) => mathUnits(r[ci] ?? ''))));
        u += colW.reduce((a, b) => a + b, 0) + cols * 1.4 + 1.5;
        i = end < 0 ? s.length : end + `\\end{${env}}`.length;
      } else if (name === 'sqrt') {
        if (s[i] === '[') i = s.indexOf(']', i) + 1 || s.length;
        const [a, j] = braceGroup(s, i);
        u += mathUnits(a) + 1.2;
        i = j;
      } else if (ZERO_WIDTH.has(name)) {
        /* the argument is counted as it is read */
      } else if (WORD_OPS.has(name)) u += name.length + 0.4;
      else if (WIDE_OPS.has(name)) u += 2;
      else if (name === 'quad') u += 2;
      else if (name === 'qquad') u += 4;
      else if (/^[,;:! ]$/.test(name)) u += 0.3;
      else u += 1.1; // greek letters and other symbols
    } else if (c === '^' || c === '_') {
      const [a, j] = braceGroup(s, i + 1);
      u += 0.7 * mathUnits(a);
      i = j;
    } else {
      if ('=<>'.includes(c)) u += 2;
      else if ('+-'.includes(c)) u += 1.8;
      else if (c !== '{' && c !== '}' && c !== ' ' && c !== '&') u += 1;
      i++;
    }
  }
  return u;
}

/** Rough printed width of an option, in average body-text characters (maths counts a little wider). */
export function optionWidth(o) {
  let units = 0;
  const prose = String(o).replace(/\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g, (_, d, t) => {
    units += 1.15 * mathUnits(d ?? t);
    return '';
  });
  return units + prose.replace(/\*\*/g, '').length;
}

/** '' (one per line), 'is-grid' (2 x 2) or 'is-grid is-row' (all four on one line), as a CBSE paper sets them. */
function optionsLayout(q) {
  if (q.type !== 'mcq' || q.options.length !== 4) return '';
  const w = Math.max(...q.options.map(optionWidth));
  if (w <= 11) return 'is-grid is-row';
  if (w <= 31) return 'is-grid';
  return '';
}

function renderOptions(q, ctx) {
  if (!Array.isArray(q.options)) return '';
  const correct = ctx?.reveal ? correctOptionIndex(q) : -1;
  const layout = optionsLayout(q);
  const items = q.options
    .map((o, i) => {
      const ok = i === correct;
      return `<li class="q-opt${ok ? ' is-correct' : ''}"><span class="q-opt-letter">${ok ? sketchCircle(seedOf(ctx, q, i)) : ''}(${LETTERS[i]})</span><span class="q-opt-text">${renderRich(o)}</span>${ok ? '<span class="visually-hidden"> (correct)</span>' : ''}</li>`;
    })
    .join('');
  return `<ol class="q-options${layout ? ` ${layout}` : ''}" type="A">${items}</ol>`;
}

function renderQuestionParts(q) {
  if (!Array.isArray(q.parts) || !q.parts.length) return '';
  const items = q.parts
    .map((p) => {
      const or = p.alt ? '<li class="q-or" aria-label="or"><span>OR</span></li>' : '';
      const m = typeof p.marks === 'number' ? `<span class="q-part-marks">${marksLabel(p.marks)}</span>` : '<span class="q-part-marks"></span>';
      return `${or}<li class="q-part${p.alt ? ' is-alt' : ''}"><span class="q-part-label">${escapeHtml(p.label)}</span><span class="q-part-text">${renderRich(p.text)}</span>${m}</li>`;
    })
    .join('');
  return `<ol class="q-parts">${items}</ol>`;
}

function renderQuestionHead(q, ctx) {
  const src = q.source ? `<span class="q-source">${renderRich(q.source)}</span>` : '';
  return `<header class="q-head"><span class="q-badge" aria-label="Question ${q.n}">${sketchCircle(seedOf(ctx, q, 9))}<span class="q-num">${q.n}</span></span><span class="q-type">${escapeHtml(typeLabel(q.type))}</span>${src}<span class="q-marks">${marksLabel(q.marks)}</span></header>`;
}

function renderQuestionBox(q, ctx) {
  const fig = q.figure
    ? inlineFigure(ctx.dir, q.figure, { cls: 'q-fig', idPrefix: figId(ctx, q, 'q'), maxWidthMm: 100, maxHeightMm: 80, alt: `Figure for question ${q.n}` })
    : '';
  return `<div class="q-box"><div class="q-text">${renderRich(q.question)}</div>${fig}${renderOptions(q, ctx)}${renderQuestionParts(q)}</div>`;
}

/** The question on its own (worksheet view / website "try it first" view). */
export function renderQuestion(q, ctx = {}) {
  return `<article class="q" id="${questionAnchor(q)}" data-type="${escapeHtml(q.type)}">${renderQuestionHead(q, ctx)}${renderQuestionBox(q, ctx)}</article>`;
}

export function renderSteps(steps, ctx = {}, q = { n: 0 }, partKey = '') {
  if (!Array.isArray(steps) || !steps.length) return '';
  const rows = steps
    .map((st, i) => {
      const math = st.math ? `<div class="step-math">${renderMath(st.math, { display: true })}</div>` : '';
      const why = st.why ? `<p class="step-why">${renderRich(st.why)}</p>` : '';
      const fig = st.figure
        ? inlineFigure(ctx.dir, st.figure, { cls: 'step-fig', idPrefix: figId(ctx, q, `s${partKey}${i}`), maxWidthMm: 110, maxHeightMm: 88, alt: `Figure for step ${i + 1}` })
        : '';
      const has = typeof st.marks === 'number' && st.marks > 0;
      const marks = has
        ? `<span class="step-marks has-marks" title="${marksLabel(st.marks)}">${sketchTick(seedOf(ctx, q, i * 7 + partKey.length))}<span class="step-mark">${marksHtml(st.marks)}</span></span>`
        : '<span class="step-marks"></span>';
      return `<li class="step"><span class="step-n">${i + 1}</span><div class="step-body"><p class="step-do">${renderRich(st.do)}</p>${math}${why}${fig}</div>${marks}</li>`;
    })
    .join('');
  return `<ol class="steps">${rows}</ol>`;
}

export function renderAnswer(html, ctx = {}, { part = false, label = 'Answer', seed = 1 } = {}) {
  if (!html) return '';
  return `<div class="answer${part ? ' answer-part' : ''}">${sketchBox(seed, { w: 600, h: part ? 38 : 46 })}<span class="answer-label">${escapeHtml(label)}</span><span class="answer-text">${html}</span></div>`;
}

function renderSolvedParts(q, ctx) {
  const qParts = new Map((q.parts || []).map((p) => [p.label, p]));
  return q.solution.parts
    .map((p, i) => {
      const qp = qParts.get(p.label);
      const marks = qp && typeof qp.marks === 'number' ? `<span class="sol-part-marks">${marksLabel(qp.marks)}</span>` : '';
      const text = ctx.showPartText && qp ? `<span class="sol-part-text">${renderRich(qp.text)}</span>` : '';
      const or = p.alt ? '<div class="sol-or"><span>OR</span></div>' : '';
      return `<div class="sol-part${p.alt ? ' is-alt' : ''}">${or}<h4 class="sol-part-head"><span class="sol-part-label">${escapeHtml(p.label)}</span>${text}${marks}</h4>${renderSteps(p.steps, ctx, q, `p${i}`)}${renderAnswer(renderRich(p.answer, { fullSize: true }), ctx, { part: true, label: `Answer ${p.label}`, seed: seedOf(ctx, q, 50 + i) })}</div>`;
    })
    .join('');
}

/** The solution on its own. */
export function renderSolution(q, ctx = {}) {
  const s = q.solution || {};
  const concept = s.concept ? `<p class="sol-concept"><span class="sol-label">Formula / idea</span> ${renderRich(s.concept)}</p>` : '';
  const fig = s.figure
    ? inlineFigure(ctx.dir, s.figure, { cls: 'sol-fig', idPrefix: figId(ctx, q, 's'), maxWidthMm: 115, maxHeightMm: 90, alt: `Figure for the solution of question ${q.n}` })
    : '';
  const hasParts = Array.isArray(s.parts) && s.parts.length;
  const body = hasParts ? renderSolvedParts(q, ctx) : renderSteps(s.steps, ctx, q);
  const answer = hasParts ? '' : renderAnswer(renderRich(s.answer, { fullSize: true }), ctx, { seed: seedOf(ctx, q, 40) });
  const watch = s.mistake ? `<p class="watch"><span class="watch-label">Watch out</span> ${renderRich(s.mistake)}</p>` : '';
  return `<section class="sol" aria-label="Solution to question ${q.n}">${concept}${fig}${body}${answer}${watch}</section>`;
}

/** Question (with the correct option marked) followed by its step-wise solution. */
export function renderSolvedQuestion(q, ctx = {}) {
  const c = { ...ctx, reveal: true };
  return `<article class="q q-solved" id="${questionAnchor(q)}" data-type="${escapeHtml(q.type)}">${renderQuestionHead(q, c)}${renderQuestionBox(q, c)}${renderSolution(q, c)}</article>`;
}

export function renderLevelHead(level, ctx = {}, idx = 0) {
  const marks = typeof level.marks === 'number' ? `<span class="level-marks">${marksLabel(level.marks)}</span>` : '';
  return `<h2 class="level-head"><span class="level-name">${escapeHtml(level.name)}${sketchUnderline((Number(ctx.chapter) || 0) * 10 + idx)}</span>${marks}</h2>`;
}
