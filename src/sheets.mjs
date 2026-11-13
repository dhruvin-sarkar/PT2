/*
 * Full HTML documents for the two A4 PDFs of one content file (used by tools/build-pdf.mjs).
 *
 * Exports
 *   solutionsHtml(entry, { assetBase })  step-wise solution sheet (main deliverable)
 *   worksheetHtml(entry, { assetBase })  question paper + answer key on a new last page
 *   solutionsTitle(doc), worksheetTitle(doc)   the PDF title metadata strings
 *   chapterHeading(doc)                  "Chapter 3: Matrices"
 *   STYLESHEETS                          the stylesheet / script files (relative to assetBase) a page needs
 *
 * entry: an item from loadContent() (src/content.mjs): { doc, dir, chapter, set }.
 * assetBase: URL of the folder holding the copied assets (docs/assets), e.g. "file:///G:/PT2/docs/assets".
 */
import { escapeHtml, renderRich, marksLabel, typeLabel } from './rich.mjs';
import { renderSolvedQuestion, renderLevelHead, renderQuestion, questionAnchor } from './components.mjs';
import { sketchUnderline, sketchTick } from './sketch.mjs';

export const STYLESHEETS = ['katex/katex.min.css', 'fonts.css', 'tokens.css', 'sheet.css', 'print.css'];

export const chapterHeading = (doc) => `Chapter ${doc.chapter}: ${doc.chapterTitle}`;
export const solutionsTitle = (doc) => `Class 12 Mathematics, ${chapterHeading(doc)} (${doc.title}), step-wise solutions`;
export const worksheetTitle = (doc) => `Class 12 Mathematics, ${chapterHeading(doc)}`;

const cssString = (s) => `"${String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, ' ')}"`;

function pageRules(left, center, right) {
  const box = `font-family: "Atkinson Hyperlegible", sans-serif; font-size: 8.5pt; color: #5d6676; vertical-align: bottom; padding-bottom: 3.2mm; border-bottom: 0.6pt solid #cdd3dc;`;
  return `
@page {
  @top-left { content: ${cssString(left)}; ${box} text-align: left; }
  @top-center { content: ${cssString(center)}; ${box} text-align: center; }
  @top-right { content: ${cssString(right)}; ${box} text-align: right; font-family: "Patrick Hand", cursive; font-size: 11pt; color: #24467f; }
  @bottom-center { content: "Page " counter(page) " of " counter(pages); font-family: "Atkinson Hyperlegible", sans-serif; font-size: 8.5pt; color: #5d6676; vertical-align: top; padding-top: 3mm; }
}
@page :first {
  @top-left { content: none; border: 0; }
  @top-center { content: none; border: 0; }
  @top-right { content: none; border: 0; }
}`;
}

function head(title, assetBase, extraCss) {
  const links = STYLESHEETS.map((s) => `<link rel="stylesheet" href="${assetBase}/${s}">`).join('\n');
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>${escapeHtml(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
${links}
<style>${extraCss}</style>
<script src="${assetBase}/fit.js"></script>
</head>`;
}

const countQuestions = (doc) => doc.levels.reduce((n, l) => n + (l.questions || []).length, 0);

export function solutionsHtml(entry, { assetBase }) {
  const { doc, dir } = entry;
  const ctx = { dir, chapter: doc.chapter, set: doc.set, idBase: 'c' };
  const levels = doc.levels
    .map((lv, i) => `<section class="level">${renderLevelHead(lv, ctx, i)}${(lv.questions || []).map((q) => renderSolvedQuestion(q, ctx)).join('\n')}</section>`)
    .join('\n');
  const nQ = countQuestions(doc);
  const legend = `<div class="legend" role="note"><p>Each row is one line of working. The red number in the right margin is what an examiner gives for that line, as in the CBSE marking scheme (½ is half a mark). Write every line that carries a mark.</p><span class="step-marks has-marks" aria-hidden="true">${sketchTick(3)}<span class="step-mark"><span class="half">½</span></span></span></div>`;
  const body = `<body>
<main class="sheet sheet-solutions">
<header class="title-block">
<p class="tb-kicker">Class 12 Mathematics</p>
<h1 class="tb-title">${escapeHtml(chapterHeading(doc))}</h1>
<p class="tb-sub">${escapeHtml(doc.title)}: step-wise solutions</p>
<p class="tb-meta"><span><b>${nQ}</b> questions</span><span><b>${escapeHtml(String(doc.totalMarks))}</b> marks</span><span><b>${doc.levels.length}</b> levels</span></p>
${sketchUnderline(doc.chapter * 7 + 1, { w: 600, h: 8 }).replace('class="sk sk-underline"', 'class="sk sk-underline tb-rule"')}
${legend}
</header>
${levels}
</main>
</body>
</html>`;
  return head(solutionsTitle(doc), assetBase, pageRules(chapterHeading(doc), doc.title, 'Step-wise solutions')) + body;
}

export function worksheetHtml(entry, { assetBase }) {
  const { doc, dir } = entry;
  const ctx = { dir, chapter: doc.chapter, set: doc.set, idBase: 'w', reveal: false };
  const rows = doc.levels
    .map((lv) => {
      const lvRow = `<tr class="ws-level"><th colspan="3">${escapeHtml(lv.name)}<span>${typeof lv.marks === 'number' ? marksLabel(lv.marks) : ''}</span></th></tr>`;
      const qs = (lv.questions || [])
        .map((q) => {
          // reuse the question card, minus its head (the table supplies number and marks)
          const card = renderQuestion(q, ctx).replace(/<header class="q-head">[\s\S]*?<\/header>/, '');
          const src = q.source ? `, ${renderRich(q.source)}` : '';
          return `<tr class="ws-row" id="${questionAnchor(q)}"><td class="ws-n">${q.n}</td><td class="ws-q"><span class="ws-type">${escapeHtml(typeLabel(q.type))}${src}</span>${card}</td><td class="ws-m">${marksLabel(q.marks)}</td></tr>`;
        })
        .join('\n');
      return `<tbody>${lvRow}${qs}</tbody>`;
    })
    .join('\n');
  const key = doc.levels
    .map((lv) => {
      const items = (lv.questions || []).map((q) => `<li><span class="key-n">${q.n}</span><span class="key-a">${renderRich(q.solution?.answer)}</span></li>`).join('');
      return `<h3 class="key-level">${escapeHtml(lv.name)}</h3><ol class="key-list">${items}</ol>`;
    })
    .join('\n');
  const body = `<body>
<main class="sheet sheet-worksheet">
<header class="title-block">
<p class="tb-kicker">${escapeHtml(doc.title)}</p>
<h1 class="tb-title tb-title-ws">${escapeHtml(worksheetTitle(doc))}</h1>
<p class="tb-meta"><span>Maximum marks: <b>${escapeHtml(String(doc.totalMarks))}</b></span><span><b>${countQuestions(doc)}</b> questions</span></p>
<div class="ws-lines"><span class="ws-line">Name <i></i></span><span class="ws-line">Date <i></i></span><span class="ws-line">Score <i></i> / ${escapeHtml(String(doc.totalMarks))}</span></div>
<ol class="ws-instr">
<li>All questions are compulsory. Marks are shown against each question.</li>
<li>Show every step of working: steps carry marks, not just the final answer.</li>
<li>Where a question offers OR, attempt only one of the two choices.</li>
</ol>
</header>
<table class="ws-table">
<colgroup><col class="c-n"><col class="c-q"><col class="c-m"></colgroup>
<thead><tr><th class="c-n">Q No.</th><th class="c-q">Question</th><th class="c-m">Marks</th></tr></thead>
${rows}
</table>
<section class="key">
<h2 class="key-title">Answer key</h2>
<p class="key-sub">${escapeHtml(chapterHeading(doc))}, ${escapeHtml(doc.title)}. Full step-wise solutions are in the solutions sheet.</p>
${key}
</section>
</main>
</body>
</html>`;
  const ws = `.tb-title-ws { font-size: var(--fs-h2); }`;
  return head(worksheetTitle(doc), assetBase, pageRules(chapterHeading(doc), doc.title, 'Worksheet') + ws) + body;
}
