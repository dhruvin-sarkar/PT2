/*
 * Website page templates (build time). Pure functions: site model in, full HTML documents out.
 * Used by tools/build-site.mjs. Question / solution markup comes from src/components.mjs; this file only wraps it.
 *
 * Exports
 *   homePage(site)                 docs/index.html
 *   chapterPage(site, chapter)     docs/chNN/index.html
 *   walkPage(site, chapter, set)   docs/chNN/<set>/index.html
 *   snippet(rich, max)             first ~max characters of contract rich text, never cutting inside $..$
 *
 * site:    { title, subtitle, chapters: [chapter] }
 * chapter: { n, dir: "ch03", title, sets: [set], questions, marks }
 * set:     { key: "ch03/school", set: "school", title, doc, dir, questions, marks,
 *            pdf: { worksheet, solutions, original } each null or { href (from docs/), pages, bytes } }
 *
 * Every URL is relative (the site lives under a sub-path on GitHub Pages and also works from file://).
 */
import { escapeHtml, renderRich, marksLabel, typeLabel } from '../rich.mjs';
import { renderQuestion, renderSolution, correctOptionIndex } from '../components.mjs';
import { sketchCircle, sketchUnderline, sketchTick } from '../sketch.mjs';
import { chapterDoodle, arrowDoodle, pageDoodle, pencilDoodle, moonDoodle, sunDoodle, starDoodle, roughBox, swipe } from './doodles.mjs';

const plural = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;
const kb = (bytes) => (bytes >= 1024 * 1024 ? `${(bytes / 1024 / 1024).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1024))} KB`);

/* ---------------------------------------------------------------- shell */

const THEME_BOOT = `(function(){var d=document.documentElement,t=null;d.className+=' js';try{t=localStorage.getItem('pt2-theme');}catch(e){}if(t!=='dark'&&t!=='light')t=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';d.setAttribute('data-theme',t);})();`;

/** Lets CSS draw a pen stroke in (stroke-dasharray: 1) on ticks and option rings. */
const drawable = (html) => html.replace(/(<svg class="sk sk-(?:tick|circle)"[^>]*>)<path /g, '$1<path pathLength="1" ');

function shell({ root, title, description, page, maths = false, body, home = false }) {
  const css = [maths ? 'katex/katex.min.css' : null, 'fonts.css', 'tokens.css', maths ? 'sheet.css' : null, 'site.css'].filter(Boolean);
  const brand = home
    ? ''
    : `<a class="brand" href="${root}index.html">${pencilDoodle(3)}<span>Class 12 Maths Sketchbook</span></a>`;
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)}</title>
<meta name="description" content="${escapeHtml(description)}">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="${root}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="${root}assets/fonts/patrick-hand-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<script>${THEME_BOOT}</script>
${css.map((c) => `<link rel="stylesheet" href="${root}assets/${c}">`).join('\n')}
${maths ? `<script defer src="${root}assets/fit.js"></script>\n` : ''}<script defer src="${root}assets/site.js"></script>
</head>
<body data-page="${page}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar${home ? ' topbar-home' : ''}">
${brand}
<button class="theme-toggle" type="button" aria-pressed="false" title="Night study theme">${moonDoodle(1)}${sunDoodle(2)}<span class="vh">Night study theme</span></button>
</header>
<main id="main" tabindex="-1">
${body}
</main>
<footer class="foot">
<p>Progress is saved in this browser only. Maths typeset with KaTeX. Questions follow the CBSE board pattern.</p>
<p><a href="${root}index.html">Contents</a></p>
</footer>
</body>
</html>
`;
}

/** Wobbly-outlined button or link. `tag` is "a" or "button". The primary style adds a highlighter swipe. */
function sketchButton({ tag = 'a', href, cls = '', label, short = '', seed = 1, attrs = '', icon = '', iconAfter = '' }) {
  const open = tag === 'a' ? `<a class="btn ${cls}" href="${href}"${attrs}>` : `<button type="button" class="btn ${cls}"${attrs}>`;
  const w = Math.round(label.length * 8.6 + 40 + (icon || iconAfter ? 30 : 0));
  const hi = /btn-primary|btn-got|btn-rev/.test(cls) ? swipe(seed + 3) : '';
  const text = short ? `<span class="btn-label"><span class="lbl-wide">${label}</span><span class="lbl-narrow" aria-hidden="true">${short}</span></span>` : `<span class="btn-label">${label}</span>`;
  return `${open}${hi}${roughBox(seed, { w, h: 46 })}${icon}${text}${iconAfter}${tag === 'a' ? '</a>' : '</button>'}`;
}

const underlined = (text, seed, cls = '') => `<span class="ul ${cls}">${text}${sketchUnderline(seed, { w: 300, h: 10 })}</span>`;

/* ---------------------------------------------------------------- snippet */

/** First ~max visible characters of contract rich text; maths is never cut, bold markers dropped. */
export function snippet(rich, max = 120) {
  const s = String(rich ?? '')
    .replace(/\*\*/g, '')
    .replace(/\$\$([\s\S]+?)\$\$/g, (_, t) => `$${t}$`)
    .replace(/\\dfrac/g, '\\frac')
    .replace(/\\displaystyle\s*/g, '');
  const re = /\$([^$]+?)\$/g;
  let out = '';
  let len = 0;
  let last = 0;
  const pushText = (t) => {
    const room = max - len;
    if (t.length <= room) {
      out += t;
      len += t.length;
      return true;
    }
    let cut = t.slice(0, Math.max(0, room));
    const sp = cut.lastIndexOf(' ');
    if (sp > room * 0.4) cut = cut.slice(0, sp);
    out = `${(out + cut).replace(/[\s,;:.(]+$/, '')}…`;
    len = max;
    return false;
  };
  let m;
  while ((m = re.exec(s))) {
    if (!pushText(s.slice(last, m.index))) return out;
    const w = Math.ceil(m[1].replace(/\\[a-zA-Z]+|[{}^_\\]/g, (x) => (x.length > 2 ? 'x' : '')).length * 0.9);
    if (len + w > max + 12) return `${out.replace(/\s+$/, '')} …`;
    out += m[0];
    len += w;
    last = re.lastIndex;
  }
  pushText(s.slice(last));
  return out;
}

/* ---------------------------------------------------------------- home */

function progressBar(seed, cls = '') {
  const w = cls.includes('pbar-lg') ? 280 : 96;
  return `<span class="pbar ${cls}" aria-hidden="true">${roughBox(seed, { w, h: cls.includes('pbar-lg') ? 24 : 14, wobble: 0.9 })}<span class="pbar-got"></span><span class="pbar-rev">${swipe(seed + 9)}</span></span>`;
}

function chapterCard(ch, i) {
  const tilt = ((((ch.n * 37) % 11) - 5) / 5) * 0.7;
  const sets = ch.sets.map((s) => `${s.key}:${s.questions}`).join(',');
  return `<li class="card-slot">
<a class="card" href="${ch.dir}/index.html" style="--tilt:${tilt.toFixed(2)}deg" data-sets="${escapeHtml(sets)}" data-total="${ch.questions}">
<span class="card-head"><span class="card-num">${sketchCircle(ch.n * 13 + 1)}<span>${ch.n}</span></span><span class="card-title">${escapeHtml(ch.title)}</span></span>
<span class="card-body">
<span class="card-line">${plural(ch.sets.length, 'set')}</span>
<span class="card-line">${plural(ch.questions, 'question')}, ${ch.marks} marks</span>
<span class="card-line card-progress">${progressBar(ch.n * 3 + i, 'pbar-sm')}<span class="card-progress-text">Not started</span></span>
</span>
${chapterDoodle(ch.n)}
</a>
</li>`;
}

export function homePage(site) {
  const totalQ = site.chapters.reduce((n, c) => n + c.questions, 0);
  const totalSets = site.chapters.reduce((n, c) => n + c.sets.length, 0);
  const steps = [
    ['Try the worksheet', 'Print the question paper, or open the walkthrough and work on paper before you reveal anything.'],
    ['Check it against the solutions', 'Every line of working is written out with the marks an examiner gives for it.'],
    ['Walk through what you got wrong', 'Go to that question and reveal the solution one step at a time. Mark it Got it or Revisit.'],
  ];
  const how = steps
    .map(
      ([h, p], i) => `<li class="how-step">
<span class="how-num">${sketchCircle(500 + i)}<span>${i + 1}</span></span>
<span class="how-text"><span class="how-h">${h}</span><span class="how-p">${p}</span></span>
${i < steps.length - 1 ? `<span class="how-arrow">${arrowDoodle(i + 3, 'right')}${arrowDoodle(i + 3, 'down')}</span>` : ''}
</li>`,
    )
    .join('\n');
  const body = `
<section class="hero" aria-labelledby="title">
<div class="hero-text">
<h1 id="title" class="hero-title">${underlined('Class 12 Maths Sketchbook', 11, 'ul-hero')}</h1>
<p class="hero-sub">${escapeHtml(site.subtitle)}</p>
<p class="hero-purpose">All ${site.chapters.length} chapters of the CBSE syllabus, with every worksheet solved line by line and the marks a board examiner gives for each line.</p>
</div>
<aside class="sticky" aria-labelledby="progress-h" data-total="${totalQ}">
<span class="tape" aria-hidden="true"></span>
<h2 id="progress-h" class="sticky-h">Your progress</h2>
${progressBar(42, 'pbar-lg')}
<p class="sticky-text" aria-live="polite"><span class="js-only">Nothing ticked off yet. Pick a chapter below and start with question 1.</span><noscript>Turn on JavaScript to keep track of the questions you have done.</noscript></p>
<p class="sticky-meta">${totalQ} questions in ${totalSets} sets</p>
</aside>
</section>

<section class="how" aria-labelledby="how-h">
<h2 id="how-h" class="sec-h">${underlined('How to use this', 21)}</h2>
<ol class="how-list">
${how}
</ol>
</section>

<section class="contents" aria-labelledby="contents-h">
<h2 id="contents-h" class="sec-h">${underlined('Chapters', 31)}</h2>
<ol class="cards">
${site.chapters.map(chapterCard).join('\n')}
</ol>
</section>`;
  return shell({
    root: '',
    title: site.title,
    description: `${site.subtitle}. ${site.chapters.length} chapters, ${totalQ} questions with step-wise solutions.`,
    page: 'home',
    body,
    home: true,
  });
}

/* ---------------------------------------------------------------- chapter */

function pdfLink(pdf, label, seed, root) {
  if (!pdf) return '';
  const meta = [pdf.pages ? plural(pdf.pages, 'page') : null, pdf.bytes ? kb(pdf.bytes) : null].filter(Boolean).join(', ');
  return `<a class="file" href="${root}${pdf.href}">${pageDoodle(seed)}<span class="file-text"><span class="file-label">${label}</span><span class="file-meta">PDF${meta ? `, ${meta}` : ''}</span></span></a>`;
}

const SET_BLURB = {
  school: 'The worksheet given out in school, solved line by line.',
};
const setBlurb = (s) => SET_BLURB[s.set] || 'More questions in the same pattern, for a second round of practice.';

function setRow(ch, s, i) {
  const root = '../';
  const files = [
    pdfLink(s.pdf.worksheet, 'Question paper', i * 3 + 1, root),
    pdfLink(s.pdf.solutions, 'Solutions', i * 3 + 2, root),
    pdfLink(s.pdf.original, 'Original school worksheet', i * 3 + 3, root),
  ].join('');
  return `<li class="set" data-key="${s.key}" data-total="${s.questions}">
<div class="set-main">
<h3 class="set-title">${escapeHtml(s.title)}</h3>
<p class="set-meta">${plural(s.questions, 'question')}, ${s.marks} marks</p>
<p class="set-blurb">${setBlurb(s)}</p>
<p class="set-progress" aria-live="polite">${progressBar(ch.n * 7 + i, 'pbar-sm')}<span class="set-progress-text">Not started</span></p>
</div>
<div class="set-actions">
${sketchButton({ href: `${s.set}/index.html`, cls: 'btn-primary', label: 'Walk through', seed: ch.n * 5 + i, iconAfter: arrowDoodle(ch.n + i, 'right') })}
<div class="files">${files}</div>
</div>
</li>`;
}

function chip(group, value, label, pressed, seed) {
  const w = Math.round(String(label).length * 8 + 28);
  return `<button type="button" class="chip" data-group="${group}" data-value="${escapeHtml(value)}" aria-pressed="${pressed ? 'true' : 'false'}">${swipe(seed + 50)}${roughBox(seed, { w, h: 36, wobble: 1.2 })}<span>${escapeHtml(label)}</span></button>`;
}

function questionList(ch) {
  const levels = [...new Set(ch.sets.flatMap((s) => s.doc.levels.map((l) => l.name)))];
  const typesPresent = new Set(ch.sets.flatMap((s) => s.doc.levels.flatMap((l) => l.questions.map((q) => q.type))));
  const types = ['mcq', 'assertion-reason', 'short', 'long', 'case'].filter((t) => typesPresent.has(t));
  for (const t of typesPresent) if (!types.includes(t)) types.push(t);
  let seed = ch.n * 100;
  const filters = `<div class="filters" role="group" aria-label="Filter the questions">
${ch.sets.length > 1 ? `<div class="fgroup" role="group" aria-labelledby="f-set"><span class="flabel" id="f-set">Set</span>${ch.sets.map((s, i) => chip('set', s.set, s.title, i === 0, seed++)).join('')}</div>` : ''}
<div class="fgroup" role="group" aria-labelledby="f-level"><span class="flabel" id="f-level">Level</span>${chip('level', '', 'All', true, seed++)}${levels.map((l) => chip('level', l, l, false, seed++)).join('')}</div>
<div class="fgroup" role="group" aria-labelledby="f-type"><span class="flabel" id="f-type">Type</span>${chip('type', '', 'All', true, seed++)}${types.map((t) => chip('type', t, typeLabel(t), false, seed++)).join('')}</div>
<div class="fgroup" role="group" aria-labelledby="f-status"><span class="flabel" id="f-status">Show</span>${chip('status', '', 'All', true, seed++)}${chip('status', 'revisit', 'To revisit', false, seed++)}${chip('status', 'todo', 'Not done yet', false, seed++)}</div>
</div>`;
  const sets = ch.sets
    .map((s) => {
      const lv = s.doc.levels
        .map((l) => {
          const rows = l.questions
            .map(
              (q) => `<li class="ql-row" data-set="${s.set}" data-level="${escapeHtml(l.name)}" data-type="${escapeHtml(q.type)}" data-n="${q.n}">
<a href="${s.set}/index.html#q${q.n}"><span class="ql-n">${q.n}</span><span class="ql-text">${renderRich(snippet(q.question, 130))}</span><span class="ql-info"><span class="ql-type">${escapeHtml(typeLabel(q.type))}</span><span class="ql-marks">${marksLabel(q.marks)}</span></span><span class="ql-state" aria-hidden="true">${sketchTick(q.n + ch.n)}</span><span class="vh ql-state-text"></span></a>
</li>`,
            )
            .join('\n');
          return `<div class="ql-level" data-level="${escapeHtml(l.name)}"><h4 class="ql-level-h">${escapeHtml(l.name)}<span>${typeof l.marks === 'number' ? marksLabel(l.marks) : ''}</span></h4><ol class="ql-list">${rows}</ol></div>`;
        })
        .join('\n');
      return `<section class="ql-set" data-set="${s.set}" data-key="${s.key}" aria-label="${escapeHtml(s.title)}"><h3 class="ql-set-h">${escapeHtml(s.title)}</h3>${lv}</section>`;
    })
    .join('\n');
  return `<section class="questions" aria-labelledby="q-h">
<h2 id="q-h" class="sec-h">${underlined('Questions', ch.n * 3 + 2)}</h2>
${filters}
<p class="ql-count" aria-live="polite"></p>
${sets}
<p class="ql-empty" hidden>No questions match these filters.</p>
</section>`;
}

export function chapterPage(site, ch) {
  const body = `
<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Contents</a><span aria-hidden="true">/</span><span aria-current="page">Chapter ${ch.n}</span></nav>
<header class="ch-head">
<span class="ch-num" aria-hidden="true">${sketchCircle(ch.n * 13 + 1)}<span>${ch.n}</span></span>
<div>
<h1 class="ch-title">${escapeHtml(ch.title)}</h1>
<p class="ch-meta">Chapter ${ch.n}. ${plural(ch.sets.length, 'set')}, ${plural(ch.questions, 'question')}, ${ch.marks} marks in all.</p>
</div>
${chapterDoodle(ch.n)}
</header>

<section class="sets" aria-labelledby="sets-h">
<h2 id="sets-h" class="vh">Worksheets</h2>
<ol class="set-list">
${ch.sets.map((s, i) => setRow(ch, s, i)).join('\n')}
</ol>
</section>

${questionList(ch)}`;
  return shell({
    root: '../',
    title: `Chapter ${ch.n}: ${ch.title} | ${site.title}`,
    description: `Class 12 Maths, Chapter ${ch.n} ${ch.title}: worksheets, step-wise solutions and walkthroughs.`,
    page: 'chapter',
    maths: true,
    body,
  });
}

/* ---------------------------------------------------------------- walkthrough */

/** Turn the static option list into buttons the student can tap (correct index goes in data-correct). */
function interactiveOptions(html, q, ctx) {
  const correct = correctOptionIndex(q);
  let i = 0;
  return html
    .replace(/<ol class="q-options([^"]*)"/, `<ol class="q-options$1" data-correct="${correct}"`)
    .replace(/<li class="q-opt">([\s\S]*?)<\/li>/g, (_, inner) => {
      const k = i++;
      const ring = sketchCircle((ctx.chapter || 0) * 1000 + q.n * 17 + k);
      const withRing = inner.replace('<span class="q-opt-letter">', `<span class="q-opt-letter">${ring}`);
      return `<li class="q-opt"><button type="button" class="opt-btn" data-i="${k}" aria-pressed="false">${withRing}<span class="opt-verdict" aria-hidden="true"></span></button></li>`;
    });
}

function picker(s, flat) {
  const levels = s.doc.levels
    .map(
      (l) => `<div class="pk-level"><p class="pk-lname">${escapeHtml(l.name)}<span>${typeof l.marks === 'number' ? marksLabel(l.marks) : ''}</span></p><ol class="pk-list">${l.questions
        .map((q) => `<li><a class="pk" href="#q${q.n}" data-n="${q.n}">${sketchCircle(q.n * 7 + 3)}<span class="pk-n">${q.n}</span><span class="vh pk-state"></span></a></li>`)
        .join('')}</ol></div>`,
    )
    .join('');
  return `<nav class="picker" aria-label="Questions in this set">
<details class="pk-wrap" open>
<summary class="pk-sum"><span class="pk-sum-text">Question <b class="pk-cur">${flat[0].q.n}</b> of ${flat.length}</span><span class="pk-sum-hint">All questions</span></summary>
<div class="pk-body">${levels}</div>
</details>
<div class="keys" aria-label="Keyboard shortcuts">
<p class="keys-h">Keys</p>
<dl>
<dt><kbd>Space</kbd> <kbd>&rarr;</kbd></dt><dd>next step</dd>
<dt><kbd>A</kbd></dt><dd>all steps</dd>
<dt><kbd>H</kbd></dt><dd>hint</dd>
<dt><kbd>N</kbd> <kbd>P</kbd></dt><dd>next or previous question</dd>
</dl>
</div>
</nav>`;
}

function walkQuestion(s, entry, i, flat, ctx) {
  const { q, level } = entry;
  const prev = flat[i - 1];
  const next = flat[i + 1];
  const hasOptions = Array.isArray(q.options) && q.options.length && correctOptionIndex(q) >= 0;
  let qHtml = renderQuestion(q, ctx).replace(` id="q${q.n}"`, ` id="q${q.n}-card"`);
  if (hasOptions) qHtml = drawable(interactiveOptions(qHtml, q, ctx));
  const sol = drawable(renderSolution(q, ctx));
  const hasHint = !!q.solution?.concept;
  const stepCount = Array.isArray(q.solution?.parts) && q.solution.parts.length ? q.solution.parts.reduce((n, p) => n + (p.steps || []).length, 0) : (q.solution?.steps || []).length;
  const seed = (ctx.chapter || 0) * 300 + q.n * 11;
  const prevLink = prev
    ? `<a class="wt-prev" href="#q${prev.q.n}" rel="prev">${arrowDoodle(seed + 1, 'right')}<span>Question ${prev.q.n}</span></a>`
    : `<a class="wt-prev" href="../index.html">${arrowDoodle(seed + 1, 'right')}<span>Chapter ${ctx.chapter}</span></a>`;
  const nextLink = next
    ? `<a class="wt-next" href="#q${next.q.n}" rel="next"><span>Question ${next.q.n}</span>${arrowDoodle(seed + 2, 'right')}</a>`
    : `<a class="wt-next" href="../index.html"><span>Back to the chapter</span>${arrowDoodle(seed + 2, 'right')}</a>`;
  return `<section class="wt-q" id="q${q.n}" data-n="${q.n}" data-steps="${stepCount}" data-marks="${q.marks}" aria-labelledby="q${q.n}-h" tabindex="-1">
<h2 class="vh" id="q${q.n}-h">Question ${q.n} of ${flat.length}, ${escapeHtml(level.name)}</h2>
<div class="slip"><span class="tape" aria-hidden="true"></span>${qHtml}</div>
${hasOptions ? `<p class="opt-feedback" aria-live="polite"><span class="js-only">Tap the option you think is right.</span></p>` : ''}
<p class="wt-try js-only">Work it out on paper first. Then reveal the solution one step at a time.</p>
<div class="wt-sol" aria-live="polite">${sol}</div>
<div class="wt-controls js-only" role="group" aria-label="Reveal the solution">
<div class="wt-buttons">
${hasHint ? sketchButton({ tag: 'button', cls: 'btn-hint', label: 'Hint', seed: seed + 3, attrs: ' data-act="hint" aria-pressed="false"' }) : ''}
${sketchButton({ tag: 'button', cls: 'btn-primary btn-next', label: 'Next step', seed: seed + 4, attrs: ' data-act="next"' })}
${sketchButton({ tag: 'button', cls: 'btn-quiet', label: 'Show all steps', short: 'All steps', seed: seed + 5, attrs: ' data-act="all" aria-label="Show all steps"' })}
${sketchButton({ tag: 'button', cls: 'btn-quiet', label: 'Show answer', short: 'Answer', seed: seed + 6, attrs: ' data-act="answer" aria-label="Show answer"' })}
</div>
<p class="wt-tally"><span class="wt-tally-steps">Step 0 of ${stepCount}</span><span class="wt-tally-marks">0 of ${marksLabel(q.marks)}</span></p>
</div>
<div class="wt-rate js-only" role="group" aria-label="How did this question go?">
<p class="wt-rate-q">How did this one go?</p>
${sketchButton({ tag: 'button', cls: 'btn-got', label: 'Got it', seed: seed + 7, attrs: ' data-rate="got" aria-pressed="false"', icon: sketchTick(seed + 8) })}
${sketchButton({ tag: 'button', cls: 'btn-rev', label: 'Revisit', seed: seed + 9, attrs: ' data-rate="revisit" aria-pressed="false"', icon: starDoodle(seed + 10) })}
</div>
<nav class="wt-nav" aria-label="Previous and next question">${prevLink}${nextLink}</nav>
</section>`;
}

export function walkPage(site, ch, s) {
  const ctx = { dir: s.dir, chapter: ch.n, set: s.set, idBase: 'w', reveal: false };
  const flat = s.doc.levels.flatMap((level) => level.questions.map((q) => ({ q, level })));
  const files = [s.pdf.worksheet ? `<a href="../../${s.pdf.worksheet.href}">Question paper PDF</a>` : '', s.pdf.solutions ? `<a href="../../${s.pdf.solutions.href}">Solutions PDF</a>` : ''].filter(Boolean).join('');
  const body = `
<nav class="crumbs" aria-label="Breadcrumb"><a href="../../index.html">Contents</a><span aria-hidden="true">/</span><a href="../index.html">Chapter ${ch.n}: ${escapeHtml(ch.title)}</a><span aria-hidden="true">/</span><span aria-current="page">${escapeHtml(s.title)}</span></nav>
<header class="wt-head">
<h1 class="wt-title">${escapeHtml(s.title)}</h1>
<p class="wt-meta">${escapeHtml(ch.title)}. ${plural(flat.length, 'question')}, ${s.marks} marks.${files ? ` <span class="wt-files">${files}</span>` : ''}</p>
</header>
<div class="wt" data-key="${s.key}" data-count="${flat.length}">
${picker(s, flat)}
<div class="wt-main">
${flat.map((e, i) => walkQuestion(s, e, i, flat, ctx)).join('\n')}
</div>
</div>`;
  return shell({
    root: '../../',
    title: `${s.title}, Chapter ${ch.n}: ${ch.title} | ${site.title}`,
    description: `Step-by-step walkthrough of ${s.title}, Class 12 Maths Chapter ${ch.n} ${ch.title}.`,
    page: 'walk',
    maths: true,
    body,
  });
}
