/*
 * Copies everything a rendered page needs into one folder (docs/assets by default):
 *
 *   <dest>/katex/katex.min.css + <dest>/katex/fonts/*.woff2   (from the katex npm package)
 *   <dest>/fonts/*.woff2 + <dest>/fonts.css                    (Atkinson Hyperlegible + Patrick Hand, from @fontsource)
 *   <dest>/tokens.css <dest>/sheet.css <dest>/print.css        (src/styles)
 *   <dest>/fit.js                                              (src/client/fit.js)
 *
 * Exports
 *   copyAssets(dest = "docs/assets") -> list of written files (relative to dest). Idempotent, only copies when changed.
 *   ASSET_DIR                         absolute path of docs/assets
 */
import fs from 'node:fs';
import path from 'node:path';
import { REPO_ROOT } from './content.mjs';

export const ASSET_DIR = path.join(REPO_ROOT, 'docs', 'assets');

const NM = path.join(REPO_ROOT, 'node_modules');
const FONT_FILES = [
  ['@fontsource/atkinson-hyperlegible/files', /^atkinson-hyperlegible-latin(-ext)?-(400|700)-(normal|italic)\.woff2$/],
  ['@fontsource/patrick-hand/files', /^patrick-hand-latin(-ext)?-400-normal\.woff2$/],
];

function copyIfChanged(src, dst, written, rel) {
  const buf = fs.readFileSync(src);
  try {
    if (fs.readFileSync(dst).equals(buf)) return;
  } catch {
    /* missing */
  }
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.writeFileSync(dst, buf);
  written.push(rel);
}

export function copyAssets(dest = ASSET_DIR) {
  const written = [];
  const kdist = path.join(NM, 'katex', 'dist');
  copyIfChanged(path.join(kdist, 'katex.min.css'), path.join(dest, 'katex', 'katex.min.css'), written, 'katex/katex.min.css');
  for (const f of fs.readdirSync(path.join(kdist, 'fonts'))) {
    if (f.endsWith('.woff2')) copyIfChanged(path.join(kdist, 'fonts', f), path.join(dest, 'katex', 'fonts', f), written, `katex/fonts/${f}`);
  }
  for (const [dir, re] of FONT_FILES) {
    for (const f of fs.readdirSync(path.join(NM, dir))) {
      if (re.test(f)) copyIfChanged(path.join(NM, dir, f), path.join(dest, 'fonts', f), written, `fonts/${f}`);
    }
  }
  const styles = path.join(REPO_ROOT, 'src', 'styles');
  for (const f of ['fonts.css', 'tokens.css', 'sheet.css', 'print.css']) copyIfChanged(path.join(styles, f), path.join(dest, f), written, f);
  copyIfChanged(path.join(REPO_ROOT, 'src', 'client', 'fit.js'), path.join(dest, 'fit.js'), written, 'fit.js');
  return written;
}
