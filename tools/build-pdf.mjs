#!/usr/bin/env node
// Builds two A4 PDFs per content file with the locally installed Edge / Chrome (puppeteer-core):
//   docs/pdf/chNN/<set>-solutions.pdf   step-wise solution sheet
//   docs/pdf/chNN/<set>-worksheet.pdf   question paper + answer key
// usage: node tools/build-pdf.mjs [--only ch01/school ...] [--force] [--content <dir>] [--out <dir>] [--browser <exe>]
//   --content defaults to content/; any other content dir defaults --out to .tmp/build/pdf so test runs
//   never land in docs/. Unchanged files (same content + renderer hash) are skipped unless --force.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer-core';
import { loadContent, chapterDir, REPO_ROOT } from '../src/content.mjs';
import { copyAssets, ASSET_DIR } from '../src/assets.mjs';
import { solutionsHtml, worksheetHtml, solutionsTitle, worksheetTitle } from '../src/sheets.mjs';

const BROWSERS = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
];

function parseArgs(argv) {
  const o = { only: [], force: false, content: null, out: null, browser: null, concurrency: 3 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => {
      const v = argv[++i];
      if (v === undefined) throw new Error(`${a} needs a value`);
      return v;
    };
    if (a === '--only') o.only.push(...val().split(',').map((s) => s.trim().replace(/\.json$/, '').replace(/\\/g, '/')));
    else if (a.startsWith('--only=')) o.only.push(...a.slice(7).split(','));
    else if (a === '--force') o.force = true;
    else if (a === '--content') o.content = val();
    else if (a === '--out') o.out = val();
    else if (a === '--browser') o.browser = val();
    else if (a === '--concurrency') o.concurrency = Math.max(1, Number(val()) || 1);
    else if (a === '-h' || a === '--help') {
      console.log('usage: node tools/build-pdf.mjs [--only ch01/school] [--force] [--content <dir>] [--out <dir>] [--browser <exe>]');
      process.exit(0);
    } else throw new Error(`unknown argument: ${a}`);
  }
  return o;
}

function rendererHash() {
  const h = crypto.createHash('sha1');
  const walk = (dir) => {
    for (const d of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const p = path.join(dir, d.name);
      if (d.isDirectory()) walk(p);
      else {
        h.update(p.slice(REPO_ROOT.length));
        h.update(fs.readFileSync(p));
      }
    }
  };
  walk(path.join(REPO_ROOT, 'src'));
  h.update(fs.readFileSync(new URL(import.meta.url)));
  for (const pkg of ['katex', '@fontsource/patrick-hand', '@fontsource/atkinson-hyperlegible']) {
    try {
      h.update(JSON.parse(fs.readFileSync(path.join(REPO_ROOT, 'node_modules', pkg, 'package.json'), 'utf8')).version);
    } catch {
      /* ignore */
    }
  }
  return h.digest('hex');
}

const countPages = (file) => (fs.readFileSync(file, 'latin1').match(/\/Type\s*\/Page(?![s\w])/g) || []).length;

async function renderPdf(browser, html, htmlFile, pdfFile, label) {
  fs.mkdirSync(path.dirname(htmlFile), { recursive: true });
  fs.writeFileSync(htmlFile, html);
  const page = await browser.newPage();
  const problems = [];
  page.on('console', (m) => {
    if (m.type() === 'error') problems.push(`console: ${m.text()}`);
  });
  page.on('requestfailed', (r) => problems.push(`failed to load ${r.url()}`));
  try {
    await page.setViewport({ width: 794, height: 1123 });
    await page.emulateMediaType('print');
    await page.goto(pathToFileURL(htmlFile).href, { waitUntil: 'load', timeout: 120000 });
    await page.evaluate(() => document.fonts.ready);
    const fonts = await page.evaluate(() => ({
      body: document.fonts.check('16px "Atkinson Hyperlegible"'),
      hand: document.fonts.check('16px "Patrick Hand"'),
    }));
    if (!fonts.body || !fonts.hand) problems.push(`web fonts not loaded: ${JSON.stringify(fonts)}`);
    const fitted = await page.evaluate(() => (window.PT ? window.PT.fitMath(document) : -1));
    if (fitted < 0) problems.push('fit.js did not load');
    const overflow = await page.evaluate(() => (window.PT ? window.PT.findOverflow(document) : []));
    for (const o of overflow) problems.push(`overflow ${o.q || '?'} ${o.cls} by ${o.over}px`);
    fs.mkdirSync(path.dirname(pdfFile), { recursive: true });
    await page.pdf({
      path: pdfFile,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: false,
      tagged: true,
      outline: true,
      timeout: 180000,
    });
    const pages = countPages(pdfFile);
    console.log(`  wrote ${path.relative(REPO_ROOT, pdfFile).replace(/\\/g, '/')}  (${pages} pages${fitted > 0 ? `, ${fitted} maths blocks fitted` : ''})`);
    for (const p of problems) console.warn(`  warn  ${label}: ${p}`);
    return { pages, problems };
  } finally {
    await page.close();
  }
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const defaultContent = path.join(REPO_ROOT, 'content');
  const contentDir = opts.content ? path.resolve(opts.content) : defaultContent;
  const isDefault = path.resolve(contentDir) === path.resolve(defaultContent);
  const outDir = opts.out ? path.resolve(opts.out) : isDefault ? path.join(REPO_ROOT, 'docs', 'pdf') : path.join(REPO_ROOT, '.tmp', 'build', 'pdf');
  const cacheDir = path.join(REPO_ROOT, '.cache');
  const cacheFile = path.join(cacheDir, 'pdf-cache.json');

  const copied = copyAssets(ASSET_DIR);
  if (copied.length) console.log(`assets: ${copied.length} files copied to docs/assets`);

  let entries = loadContent({ contentDir, log: (m) => console.warn(`warn  ${m}`) });
  if (opts.only.length) {
    const want = new Set(opts.only);
    entries = entries.filter((e) => want.has(e.key));
    for (const k of want) if (!entries.some((e) => e.key === k)) console.warn(`warn  --only ${k}: no valid content file with that key`);
  }
  if (!entries.length) {
    console.log('build-pdf: nothing to build (no valid content files).');
    return;
  }

  let cache = {};
  try {
    cache = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
  } catch {
    cache = {};
  }
  const rHash = rendererHash();
  const outKey = (e) => `${path.relative(REPO_ROOT, outDir).replace(/\\/g, '/')}::${e.key}`;
  const files = (e) => ({
    solutions: path.join(outDir, chapterDir(e.chapter), `${e.set}-solutions.pdf`),
    worksheet: path.join(outDir, chapterDir(e.chapter), `${e.set}-worksheet.pdf`),
  });
  const todo = entries.filter((e) => {
    const f = files(e);
    const want = `${e.hash}:${rHash}`;
    const fresh = cache[outKey(e)]?.hash === want && fs.existsSync(f.solutions) && fs.existsSync(f.worksheet);
    if (fresh && !opts.force) console.log(`skip  ${e.key} (unchanged)`);
    return opts.force || !fresh;
  });

  if (todo.length) {
    const exe = opts.browser || process.env.PT_BROWSER || BROWSERS.find((b) => fs.existsSync(b));
    if (!exe) throw new Error('No browser found. Pass --browser <path to msedge.exe or chrome.exe>.');
    const tmp = path.join(REPO_ROOT, '.tmp', 'browser-tmp');
    fs.mkdirSync(tmp, { recursive: true });
    // A fresh profile per run: a profile left locked by a killed run stops the browser from launching.
    const profile = path.join(cacheDir, `browser-profile-${process.pid}`);
    const browser = await puppeteer.launch({
      executablePath: exe,
      headless: true,
      userDataDir: profile,
      env: { ...process.env, TEMP: tmp, TMP: tmp },
      args: ['--no-first-run', '--no-default-browser-check', '--disable-extensions', '--allow-file-access-from-files', '--font-render-hinting=none', '--disable-gpu'],
    });
    const assetBase = pathToFileURL(ASSET_DIR).href;
    try {
      const queue = [...todo];
      const worker = async () => {
        for (let e = queue.shift(); e; e = queue.shift()) {
          console.log(`build ${e.key}  (${e.rel})`);
          const f = files(e);
          const base = path.join(cacheDir, 'html', `${chapterDir(e.chapter)}-${e.set}`);
          const s = await renderPdf(browser, solutionsHtml(e, { assetBase }), `${base}-solutions.html`, f.solutions, `${e.key} solutions`);
          const w = await renderPdf(browser, worksheetHtml(e, { assetBase }), `${base}-worksheet.html`, f.worksheet, `${e.key} worksheet`);
          cache[outKey(e)] = { hash: `${e.hash}:${rHash}`, built: new Date().toISOString(), pages: { solutions: s.pages, worksheet: w.pages }, warnings: s.problems.length + w.problems.length };
          fs.mkdirSync(cacheDir, { recursive: true });
          fs.writeFileSync(cacheFile, JSON.stringify(cache, null, 2));
        }
      };
      await Promise.all(Array.from({ length: Math.min(opts.concurrency, todo.length) }, worker));
    } finally {
      await browser.close();
      fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 300 });
    }
  }

  // Manifest of every built PDF in this output folder (the website reads docs/pdf/manifest.json).
  const all = loadContent({ contentDir, log: () => {} });
  const manifest = all
    .map((e) => {
      const f = files(e);
      if (!fs.existsSync(f.solutions) || !fs.existsSync(f.worksheet)) return null;
      const rel = (p) => path.relative(outDir, p).replace(/\\/g, '/');
      return {
        key: e.key,
        chapter: e.chapter,
        chapterTitle: e.doc.chapterTitle,
        set: e.set,
        title: e.doc.title,
        totalMarks: e.doc.totalMarks,
        questions: e.doc.levels.reduce((n, l) => n + l.questions.length, 0),
        solutions: { file: rel(f.solutions), title: solutionsTitle(e.doc), pages: countPages(f.solutions), bytes: fs.statSync(f.solutions).size },
        worksheet: { file: rel(f.worksheet), title: worksheetTitle(e.doc), pages: countPages(f.worksheet), bytes: fs.statSync(f.worksheet).size },
      };
    })
    .filter(Boolean);
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({ generated: new Date().toISOString(), items: manifest }, null, 2));
  console.log(`build-pdf: ${todo.length} built, ${entries.length - todo.length} unchanged, manifest has ${manifest.length} sets -> ${path.relative(REPO_ROOT, outDir).replace(/\\/g, '/')}`);
}

main().catch((e) => {
  console.error(`build-pdf failed: ${e.stack || e.message}`);
  process.exit(1);
});
