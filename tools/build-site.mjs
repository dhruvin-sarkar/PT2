#!/usr/bin/env node
// Builds the static website into docs/ (GitHub Pages serves that folder under a sub-path, so every URL is relative):
//   docs/index.html                 contents page: the chapters as index cards, how to use, overall progress
//   docs/chNN/index.html            chapter page: every set with its PDFs and walkthrough, filterable question list
//   docs/chNN/<set>/index.html      walkthrough: one question at a time, solution revealed step by step
//   docs/assets/site.css, site.js, favicon.svg  (+ fonts, KaTeX, tokens, sheet.css, fit.js via src/assets.mjs)
//   docs/pdf/chNN/school-original.pdf           copied from source/school/chNN-*.pdf
//   docs/.nojekyll
// Maths is rendered here with KaTeX; the browser only runs src/site/site.js (reveal, filters, progress).
// usage: node tools/build-site.mjs [--content <dir>] [--out <dir>]
import fs from 'node:fs';
import path from 'node:path';
import { loadContent, chapterDir, REPO_ROOT } from '../src/content.mjs';
import { copyAssets } from '../src/assets.mjs';
import { homePage, chapterPage, walkPage } from '../src/site/pages.mjs';
import { faviconSvg } from '../src/site/doodles.mjs';

const SITE = {
  title: 'Class 12 Maths Sketchbook',
  subtitle: 'Worksheets, step-wise solutions and walkthroughs for CBSE / NCERT',
};

function parseArgs(argv) {
  const o = { content: path.join(REPO_ROOT, 'content'), out: path.join(REPO_ROOT, 'docs') };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--content') o.content = path.resolve(argv[++i]);
    else if (a === '--out') o.out = path.resolve(argv[++i]);
    else if (a === '-h' || a === '--help') {
      console.log('usage: node tools/build-site.mjs [--content <dir>] [--out <dir>]');
      process.exit(0);
    } else throw new Error(`unknown argument: ${a}`);
  }
  return o;
}

function writeIfChanged(file, data, stats) {
  const buf = Buffer.isBuffer(data) ? data : Buffer.from(data);
  try {
    if (fs.readFileSync(file).equals(buf)) {
      stats.same++;
      return;
    }
  } catch {
    /* new file */
  }
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, buf);
  stats.written++;
}

const countPages = (file) => (fs.readFileSync(file, 'latin1').match(/\/Type\s*\/Page(?![s\w])/g) || []).length;

/** { href (relative to docs/), pages, bytes } or null when the file does not exist. */
function pdfInfo(outDir, rel, manifestItem) {
  const file = path.join(outDir, rel);
  if (!fs.existsSync(file)) return null;
  const bytes = fs.statSync(file).size;
  let pages = manifestItem?.pages;
  if (!pages || manifestItem?.bytes !== bytes) {
    try {
      pages = countPages(file);
    } catch {
      pages = 0;
    }
  }
  return { href: rel.replace(/\\/g, '/'), pages, bytes };
}

function copyOriginal(ch, outDir, stats) {
  const srcDir = path.join(REPO_ROOT, 'source', 'school');
  if (!fs.existsSync(srcDir)) return null;
  const name = fs.readdirSync(srcDir).find((f) => f.startsWith(`${chapterDir(ch)}-`) && f.toLowerCase().endsWith('.pdf'));
  if (!name) return null;
  const rel = `pdf/${chapterDir(ch)}/school-original.pdf`;
  writeIfChanged(path.join(outDir, rel), fs.readFileSync(path.join(srcDir, name)), stats);
  return rel;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  const outDir = opts.out;
  const stats = { written: 0, same: 0 };

  // shared assets (fonts, KaTeX, tokens, sheet.css, fit.js) + the site's own
  const assetDir = path.join(outDir, 'assets');
  copyAssets(assetDir);
  const siteSrc = path.join(REPO_ROOT, 'src', 'site');
  for (const f of ['site.css', 'site.js']) writeIfChanged(path.join(assetDir, f), fs.readFileSync(path.join(siteSrc, f)), stats);
  writeIfChanged(path.join(assetDir, 'favicon.svg'), faviconSvg(), stats);
  writeIfChanged(path.join(outDir, '.nojekyll'), '', stats);

  const entries = loadContent({ contentDir: opts.content, log: (m) => console.warn(`warn  ${m}`) });
  if (!entries.length) {
    console.log('build-site: no valid content files; nothing to build.');
    return;
  }

  let manifest = [];
  try {
    manifest = JSON.parse(fs.readFileSync(path.join(outDir, 'pdf', 'manifest.json'), 'utf8')).items || [];
  } catch {
    console.warn('warn  docs/pdf/manifest.json not found; PDF links come from the files on disk only');
  }
  const byKey = new Map(manifest.map((m) => [m.key, m]));

  // site model
  const chapters = new Map();
  for (const e of entries) {
    const n = e.chapter;
    if (!chapters.has(n)) chapters.set(n, { n, dir: chapterDir(n), title: e.doc.chapterTitle, sets: [], questions: 0, marks: 0 });
    const ch = chapters.get(n);
    const questions = e.doc.levels.reduce((k, l) => k + (l.questions || []).length, 0);
    const m = byKey.get(e.key);
    const pdfBase = `pdf/${chapterDir(n)}/${e.set}`;
    const set = {
      key: e.key,
      set: e.set,
      title: e.doc.title,
      doc: e.doc,
      dir: e.dir,
      questions,
      marks: e.doc.totalMarks,
      pdf: {
        worksheet: pdfInfo(outDir, `${pdfBase}-worksheet.pdf`, m?.worksheet),
        solutions: pdfInfo(outDir, `${pdfBase}-solutions.pdf`, m?.solutions),
        original: null,
      },
    };
    if (e.set === 'school') {
      const rel = copyOriginal(n, outDir, stats);
      if (rel) set.pdf.original = pdfInfo(outDir, rel, null);
    }
    ch.sets.push(set);
    ch.questions += questions;
    ch.marks += Number(e.doc.totalMarks) || 0;
  }
  const site = { ...SITE, chapters: [...chapters.values()].sort((a, b) => a.n - b.n) };

  // remove pages of chapters / sets that no longer exist (only folders this script owns: docs/chNN)
  for (const d of fs.readdirSync(outDir, { withFileTypes: true })) {
    if (!d.isDirectory() || !/^ch\d{2}$/.test(d.name)) continue;
    const ch = site.chapters.find((c) => c.dir === d.name);
    if (!ch) {
      fs.rmSync(path.join(outDir, d.name), { recursive: true, force: true });
      continue;
    }
    for (const s of fs.readdirSync(path.join(outDir, d.name), { withFileTypes: true })) {
      if (s.isDirectory() && !ch.sets.some((x) => x.set === s.name)) fs.rmSync(path.join(outDir, d.name, s.name), { recursive: true, force: true });
    }
  }

  writeIfChanged(path.join(outDir, 'index.html'), homePage(site), stats);
  let pages = 1;
  let missingPdf = 0;
  for (const ch of site.chapters) {
    writeIfChanged(path.join(outDir, ch.dir, 'index.html'), chapterPage(site, ch), stats);
    pages++;
    for (const s of ch.sets) {
      writeIfChanged(path.join(outDir, ch.dir, s.set, 'index.html'), walkPage(site, ch, s), stats);
      pages++;
      if (!s.pdf.worksheet || !s.pdf.solutions) {
        missingPdf++;
        console.warn(`warn  ${s.key}: ${!s.pdf.solutions ? 'solutions' : 'worksheet'} PDF not built yet, link left out (run npm run build:pdf)`);
      }
    }
  }
  const nSets = site.chapters.reduce((k, c) => k + c.sets.length, 0);
  console.log(`build-site: ${pages} pages for ${site.chapters.length} chapters / ${nSets} sets -> ${path.relative(REPO_ROOT, outDir).replace(/\\/g, '/') || '.'} (${stats.written} files written, ${stats.same} unchanged${missingPdf ? `, ${missingPdf} sets without PDFs` : ''})`);
}

try {
  main();
} catch (e) {
  console.error(`build-site failed: ${e.stack || e.message}`);
  process.exit(1);
}
