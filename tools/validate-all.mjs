#!/usr/bin/env node
// Validates every content/chNN/*.json with tools/validate.mjs.
// usage: node tools/validate-all.mjs [--content <dir>] [--warn-only]
//   --warn-only: report failures but exit 0 (used by "npm run build", which skips failing files).
import path from 'node:path';
import { listContentFiles, validateFiles, REPO_ROOT } from '../src/content.mjs';

const args = process.argv.slice(2);
const warnOnly = args.includes('--warn-only');
const ci = args.indexOf('--content');
const contentDir = ci >= 0 ? path.resolve(args[ci + 1]) : path.join(REPO_ROOT, 'content');

const files = listContentFiles(contentDir);
if (!files.length) {
  console.log(`validate: no content files in ${path.relative(REPO_ROOT, contentDir) || '.'}`);
  process.exit(0);
}
const res = validateFiles(files);
let bad = 0;
for (const f of files) {
  const r = res.get(path.resolve(f));
  if (!r.ok) bad++;
  for (const line of r.lines) console.log(line);
}
console.log(`validate: ${files.length - bad} of ${files.length} files pass${bad ? `, ${bad} fail${warnOnly ? ' (they will be skipped)' : ''}` : ''}`);
process.exit(bad && !warnOnly ? 1 : 0);
