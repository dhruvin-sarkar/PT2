#!/usr/bin/env node
// Checks worksheet content files against tools/CONTRACT.md.
// usage (from repo root): node tools/validate.mjs content/ch01/school.json [more.json ...]
import fs from 'node:fs';
import path from 'node:path';
import katex from 'katex';

const TYPES = ['mcq', 'assertion-reason', 'short', 'long', 'case'];
const MATH = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
const CONTROL = /[\u0000-\u001f]/;
const STRAY_TEX = /\\(d?frac|sqrt|int|sum|vec|hat|theta|alpha|beta|pi|le|ge|ne|neq|times|cdot|in|Rightarrow|begin|left|right)\b/;

const files = process.argv.slice(2);
if (!files.length) {
  console.error('usage: node tools/validate.mjs <content.json> [...]');
  process.exit(2);
}

let failed = 0;
for (const file of files) {
  const errs = [];
  const warns = [];
  let doc;
  try {
    doc = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    console.log(`FAIL ${file}\n  invalid JSON: ${e.message}`);
    failed++;
    continue;
  }
  const dir = path.dirname(file);

  const tex = (at, src, displayMode) => {
    if (CONTROL.test(src)) {
      errs.push(`${at}: control character inside math — a LaTeX backslash was not doubled in the JSON  <<  ${JSON.stringify(src).slice(0, 90)}`);
      return;
    }
    try {
      katex.renderToString(src, { throwOnError: true, displayMode, strict: 'ignore' });
    } catch (e) {
      errs.push(`${at}: KaTeX: ${String(e.message).split('\n')[0]}  <<  ${src.slice(0, 90)}`);
    }
  };

  const rich = (at, s, { required = true, maxWords = 0 } = {}) => {
    if (s === undefined || s === null || s === '') {
      if (required) errs.push(`${at}: missing`);
      return;
    }
    if (typeof s !== 'string') return void errs.push(`${at}: must be a string`);
    if (CONTROL.test(s)) return void errs.push(`${at}: control character or line break — a LaTeX backslash was not doubled in the JSON  <<  ${JSON.stringify(s).slice(0, 90)}`);
    for (const m of s.matchAll(MATH)) tex(at, m[1] ?? m[2], m[1] !== undefined);
    const prose = s.replace(MATH, ' x ');
    if (prose.includes('$')) errs.push(`${at}: unbalanced $`);
    if (/<\/?[a-z][^>]*>/i.test(prose)) errs.push(`${at}: HTML is not allowed`);
    if (STRAY_TEX.test(prose)) errs.push(`${at}: LaTeX command outside $…$`);
    if (maxWords) {
      const n = prose.trim().split(/\s+/).filter(Boolean).length;
      if (n > maxWords) warns.push(`${at}: ${n} words — aim for ${maxWords} or fewer`);
    }
  };

  const fig = (at, p) => {
    if (p === undefined) return;
    if (typeof p !== 'string' || !fs.existsSync(path.join(dir, p))) errs.push(`${at}: figure not found: ${p}`);
  };

  const checkSteps = (at, list) => {
    if (!Array.isArray(list) || !list.length) {
      errs.push(`${at}: needs a non-empty "steps" array`);
      return 0;
    }
    let sum = 0;
    list.forEach((st, i) => {
      const a = `${at} step ${i + 1}`;
      rich(`${a} do`, st.do, { maxWords: 18 });
      if (st.math !== undefined) {
        if (typeof st.math !== 'string' || !st.math.trim()) errs.push(`${a} math: must be non-empty LaTeX`);
        else if (/^\s*\$/.test(st.math)) errs.push(`${a} math: no $ delimiters in "math"`);
        else {
          tex(`${a} math`, st.math, true);
          const rows = st.math.split('\\\\').length;
          if (/\\begin\{aligned\}/.test(st.math) && rows > 5) warns.push(`${a} math: ${rows} lines — split into two steps`);
        }
      }
      rich(`${a} why`, st.why, { required: false, maxWords: 14 });
      fig(`${a} figure`, st.figure);
      if (st.marks !== undefined) {
        if (typeof st.marks !== 'number' || st.marks <= 0 || (st.marks * 2) % 1 !== 0) errs.push(`${a} marks: must be a positive multiple of 0.5`);
        else sum += st.marks;
      }
    });
    return sum;
  };

  for (const k of ['chapter', 'chapterTitle', 'set', 'title', 'totalMarks', 'levels']) {
    if (doc[k] === undefined) errs.push(`top-level "${k}" missing`);
  }
  if (doc.set && path.basename(file, '.json') !== doc.set) errs.push(`"set" is "${doc.set}" but the file is ${path.basename(file)}`);

  let total = 0;
  let count = 0;
  const seen = new Set();
  for (const [li, lv] of (Array.isArray(doc.levels) ? doc.levels : []).entries()) {
    let lvSum = 0;
    if (!lv.name) errs.push(`levels[${li}]: "name" missing`);
    if (!Array.isArray(lv.questions) || !lv.questions.length) errs.push(`${lv.name || `levels[${li}]`}: no questions`);
    for (const q of lv.questions || []) {
      const at = `Q${q.n}`;
      count++;
      if (!Number.isInteger(q.n) || seen.has(q.n)) errs.push(`${at}: "n" must be a unique integer`);
      seen.add(q.n);
      if (typeof q.marks !== 'number' || q.marks <= 0) errs.push(`${at}: "marks" missing`);
      else lvSum += q.marks;
      if (!TYPES.includes(q.type)) errs.push(`${at}: "type" must be one of ${TYPES.join(' | ')}`);
      rich(`${at} question`, q.question);
      rich(`${at} source`, q.source, { required: false });
      fig(`${at} figure`, q.figure);
      const needsOptions = q.type === 'mcq' || q.type === 'assertion-reason';
      if (needsOptions) {
        if (!Array.isArray(q.options) || q.options.length !== 4) errs.push(`${at}: exactly 4 options (A–D) required`);
        else q.options.forEach((o, i) => {
          rich(`${at} option ${'ABCD'[i]}`, o);
          if (typeof o === 'string' && /^\s*\(?[A-Da-d][).]\s/.test(o)) errs.push(`${at} option ${'ABCD'[i]}: leave out the letter`);
        });
      } else if (q.options !== undefined) errs.push(`${at}: "options" only belongs on mcq / assertion-reason`);
      for (const [i, p] of (q.parts || []).entries()) {
        if (!p.label) errs.push(`${at} part ${i + 1}: "label" missing`);
        rich(`${at} part ${p.label || i + 1} text`, p.text);
      }

      const s = q.solution;
      if (!s || typeof s !== 'object') {
        errs.push(`${at}: "solution" missing`);
        continue;
      }
      rich(`${at} answer`, s.answer);
      rich(`${at} concept`, s.concept, { required: false, maxWords: 24 });
      rich(`${at} mistake`, s.mistake, { required: false, maxWords: 28 });
      fig(`${at} solution figure`, s.figure);
      let got = 0;
      if (Array.isArray(s.parts) && s.parts.length) {
        if (s.steps !== undefined) errs.push(`${at}: use "steps" or "parts" in the solution, not both`);
        const labels = new Set((q.parts || []).map((p) => p.label));
        for (const [i, p] of s.parts.entries()) {
          const pa = `${at}${p.label || ` part ${i + 1}`}`;
          if (!p.label) errs.push(`${pa}: "label" missing`);
          else if (labels.size && !labels.has(p.label)) errs.push(`${pa}: no question part with this label`);
          const m = checkSteps(pa, p.steps);
          rich(`${pa} answer`, p.answer);
          if (!p.alt) got += m;
        }
        for (const l of labels) if (!s.parts.some((p) => p.label === l)) errs.push(`${at}${l}: part is not solved`);
      } else {
        if (Array.isArray(q.parts) && q.parts.length) errs.push(`${at}: question has parts, so the solution needs "parts" too`);
        got = checkSteps(at, s.steps);
      }
      if (typeof q.marks === 'number' && got !== q.marks) errs.push(`${at}: step marks add up to ${got}, the question carries ${q.marks}`);
    }
    if (typeof lv.marks !== 'number') errs.push(`${lv.name}: "marks" missing`);
    else if (lv.marks !== lvSum) errs.push(`${lv.name}: declared ${lv.marks} marks, questions add up to ${lvSum}`);
    total += lvSum;
  }
  if (typeof doc.totalMarks === 'number' && doc.totalMarks !== total) errs.push(`"totalMarks" is ${doc.totalMarks}, questions add up to ${total}`);

  if (errs.length) failed++;
  console.log(`${errs.length ? 'FAIL' : 'PASS'} ${file} — ${count} questions, ${total} marks, ${errs.length} errors, ${warns.length} warnings`);
  for (const e of errs) console.log(`  error  ${e}`);
  for (const w of warns) console.log(`  warn   ${w}`);
}
process.exit(failed ? 1 : 0);
