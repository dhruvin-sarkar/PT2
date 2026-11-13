/*
 * Content loader shared by the PDF build and the website build.
 *
 * Exports
 *   listContentFiles(contentDir = "content")   absolute paths of every chNN/*.json, sorted (see compareEntries)
 *   validateFiles(files)                       runs tools/validate.mjs once over all files; returns
 *                                              Map(file -> { ok, lines: [..output lines..] })
 *   loadContent({ contentDir, validate = true, log = console.warn })
 *                                              -> [{ file, dir, rel, chapter, set, key, doc, hash, figures }]
 *                                              A file that fails validation (or does not parse) is skipped with a
 *                                              clear warning; the build never crashes because of content.
 *   setRank(set)                               school -> 0, practice-a -> 1, practice-b -> 2, ... others last
 *   compareEntries(a, b)                       chapter, then set (school first, then practice-a, practice-b, ...)
 *   contentHash(entry, extra = "")             sha1 of the JSON + every referenced figure (+ extra)
 *   figurePaths(doc)                           every figure path referenced by a document
 *   chapterDir(n)                              3 -> "ch03"
 *
 * entry.key is "ch03/school"; entry.dir is the folder of the JSON (figures resolve against it).
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const VALIDATOR = path.join(ROOT, 'tools', 'validate.mjs');

export const chapterDir = (n) => `ch${String(n).padStart(2, '0')}`;

export function setRank(set) {
  if (set === 'school') return 0;
  const m = /^practice-([a-z])$/.exec(set || '');
  if (m) return 1 + m[1].charCodeAt(0) - 97;
  return 100;
}

export function compareEntries(a, b) {
  return a.chapter - b.chapter || setRank(a.set) - setRank(b.set) || String(a.set).localeCompare(String(b.set));
}

export function listContentFiles(contentDir = path.join(ROOT, 'content')) {
  const base = path.resolve(ROOT, contentDir);
  if (!fs.existsSync(base)) return [];
  const out = [];
  for (const d of fs.readdirSync(base, { withFileTypes: true })) {
    if (!d.isDirectory() || !/^ch\d{2}$/.test(d.name)) continue;
    const dir = path.join(base, d.name);
    for (const f of fs.readdirSync(dir)) if (f.endsWith('.json')) out.push(path.join(dir, f));
  }
  return out.sort((a, b) =>
    compareEntries(
      { chapter: Number(path.basename(path.dirname(a)).slice(2)), set: path.basename(a, '.json') },
      { chapter: Number(path.basename(path.dirname(b)).slice(2)), set: path.basename(b, '.json') },
    ),
  );
}

/** Runs the contract validator once over all files (its rules stay the single source of truth). */
export function validateFiles(files) {
  const result = new Map();
  if (!files.length) return result;
  const rels = files.map((f) => path.relative(ROOT, f));
  let stdout = '';
  try {
    stdout = execFileSync(process.execPath, [VALIDATOR, ...rels], { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  } catch (e) {
    stdout = String(e.stdout || '');
    if (!stdout) {
      for (const f of files) result.set(f, { ok: false, lines: [`validator could not run: ${e.message}`] });
      return result;
    }
  }
  // Output: "PASS|FAIL <file> — ..." followed by indented detail lines.
  let current = null;
  for (const line of stdout.split(/\r?\n/)) {
    const m = /^(PASS|FAIL) (.+?)(?: — |$)/.exec(line);
    if (m) {
      const abs = path.resolve(ROOT, m[2].trim());
      current = { ok: m[1] === 'PASS', lines: [line] };
      result.set(abs, current);
    } else if (current && line.trim()) current.lines.push(line);
  }
  for (const f of files) if (!result.has(path.resolve(f))) result.set(path.resolve(f), { ok: false, lines: ['no result from validator'] });
  return result;
}

export function figurePaths(doc) {
  const out = new Set();
  const add = (p) => p && out.add(p);
  for (const lv of doc.levels || []) {
    for (const q of lv.questions || []) {
      add(q.figure);
      const s = q.solution || {};
      add(s.figure);
      for (const st of s.steps || []) add(st.figure);
      for (const p of s.parts || []) for (const st of p.steps || []) add(st.figure);
    }
  }
  return [...out];
}

export function contentHash(entry, extra = '') {
  const h = crypto.createHash('sha1');
  h.update(fs.readFileSync(entry.file));
  for (const p of figurePaths(entry.doc).sort()) {
    h.update(`\0${p}\0`);
    try {
      h.update(fs.readFileSync(path.join(entry.dir, p)));
    } catch {
      h.update('missing');
    }
  }
  h.update(extra);
  return h.digest('hex');
}

export function loadContent({ contentDir = path.join(ROOT, 'content'), validate = true, log = (m) => console.warn(m) } = {}) {
  const files = listContentFiles(contentDir);
  const checks = validate ? validateFiles(files) : new Map();
  const entries = [];
  for (const file of files) {
    const rel = path.relative(ROOT, file).replace(/\\/g, '/');
    if (validate) {
      const v = checks.get(path.resolve(file));
      if (!v || !v.ok) {
        const detail = (v?.lines || []).slice(1, 6).map((l) => `    ${l.trim()}`).join('\n');
        log(`skip ${rel}: fails validation (run: node tools/validate.mjs ${rel})${detail ? `\n${detail}` : ''}`);
        continue;
      }
    }
    let doc;
    try {
      doc = JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
      log(`skip ${rel}: invalid JSON (${e.message})`);
      continue;
    }
    const chapter = Number(doc.chapter);
    const set = String(doc.set);
    const entry = { file, dir: path.dirname(file), rel, chapter, set, key: `${chapterDir(chapter)}/${set}`, doc };
    entry.figures = figurePaths(doc);
    entry.hash = contentHash(entry);
    entries.push(entry);
  }
  return entries.sort(compareEntries);
}

export const REPO_ROOT = ROOT;
