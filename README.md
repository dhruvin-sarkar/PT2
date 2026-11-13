# Class 12 Maths Sketchbook

Revision material for Class 12 CBSE Mathematics, all 13 chapters. Each chapter has the school worksheet and practice sets in the same pattern, with:

- a **question paper PDF** (questions and an answer key),
- a **solutions PDF** with every line of working and the marks a board examiner gives for each line,
- a **walkthrough** on the website that shows one question at a time and reveals the solution one step at a time.

Live site: https://dhruvin-sarkar.github.io/PT2/

Every question is written once, as JSON, and the PDFs and the website are generated from it.

## Folder layout

```
content/chNN/<set>.json   questions and step-wise solutions (school, practice-a, practice-b, ...)
content/chNN/figs/        figures as SVG, with the Python scripts that draw them
source/school/            the original school worksheets (PDF)
src/                      shared renderer: loader, rich text and KaTeX, question / solution HTML, print styles
src/site/                 website pages, styles and the small browser script
tools/                    validate, build-pdf, build-site, serve; CONTRACT.md describes the JSON format
docs/                     the built site that GitHub Pages serves (do not edit by hand)
docs/pdf/chNN/            built PDFs, plus school-original.pdf copied from source/school/
```

## Commands

Needs Node.js 20 or newer and Google Chrome (used headless to print the PDFs). Run `npm install` once.

| Command | What it does |
| --- | --- |
| `npm run validate` | Checks every `content/chNN/*.json` against `tools/CONTRACT.md`. |
| `npm run build:pdf` | Builds `docs/pdf/chNN/<set>-worksheet.pdf` and `<set>-solutions.pdf`. Unchanged sets are skipped; add `-- --force` to rebuild all, or `-- --only ch03/school` for one set. |
| `npm run build:site` | Builds the website into `docs/`: home page, a page per chapter and a walkthrough per set. |
| `npm run build` | Validate, then the PDFs, then the site. |
| `npm run serve` | Serves `docs/` at http://localhost:8080/ (`-- --port 3000` to change the port). |

To add a practice set, save it as `content/chNN/practice-x.json`, run `npm run validate`, then `npm run build`. The chapter page and the home page pick it up on their own.

## Notes

- Every link in the site is relative, so it works under the `/PT2/` sub-path and from a local server.
- Progress ("Got it" / "Revisit") is kept in the browser's local storage only.
- Maths is typeset with KaTeX when the site is built, so pages need no maths script in the browser.
