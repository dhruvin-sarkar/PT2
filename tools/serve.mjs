#!/usr/bin/env node
// Tiny static file server for the built site (docs/). No dependencies.
// usage: node tools/serve.mjs [--port 8080] [--dir docs]
// Folders serve their index.html, like GitHub Pages. Only files inside the folder are served.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { REPO_ROOT } from '../src/content.mjs';

const args = process.argv.slice(2);
const arg = (name, dflt) => {
  const i = args.indexOf(name);
  return i >= 0 && args[i + 1] ? args[i + 1] : dflt;
};
const port = Number(arg('--port', process.env.PORT || 8080));
const dir = path.resolve(REPO_ROOT, arg('--dir', 'docs'));

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.pdf': 'application/pdf',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf',
  '.txt': 'text/plain; charset=utf-8',
};

const server = http.createServer((req, res) => {
  let rel;
  try {
    rel = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  } catch {
    res.writeHead(400).end('bad request');
    return;
  }
  let file = path.join(dir, path.normalize(rel));
  if (!file.startsWith(dir)) {
    res.writeHead(403).end('forbidden');
    return;
  }
  try {
    if (fs.statSync(file).isDirectory()) {
      if (!rel.endsWith('/')) {
        res.writeHead(301, { Location: `${rel}/` }).end();
        return;
      }
      file = path.join(file, 'index.html');
    }
    const body = fs.readFileSync(file);
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }).end(`not found: ${rel}`);
  }
});

server.listen(port, () => {
  console.log(`serving ${path.relative(REPO_ROOT, dir) || '.'} at http://localhost:${port}/  (Ctrl+C to stop)`);
});
