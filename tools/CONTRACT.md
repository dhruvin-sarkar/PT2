# Content contract

Every worksheet (the school's originals and our practice sets) is stored once, as JSON, and everything else
(solution PDFs, question-paper PDFs, the website walkthrough) is generated from it.

- File location: `content/chNN/<set>.json` — `NN` is the two-digit chapter number, `<set>` is `school`, `practice-a`, `practice-b`, …
- Figures: `content/chNN/figs/<name>.svg`, referenced as `figs/<name>.svg`.
- Check a file with `node tools/validate.mjs content/chNN/<set>.json` (run from the repo root). It must print `PASS`.

## Shape

```jsonc
{
  "chapter": 1,
  "chapterTitle": "Relations and Functions",
  "set": "school",                       // same as the file name
  "title": "School Worksheet",           // "Practice Set A" etc. for practice sets
  "totalMarks": 52,
  "levels": [
    {
      "name": "Level 1",
      "marks": 8,                        // must equal the sum of its questions' marks
      "questions": [
        {
          "n": 1,
          "marks": 1,
          "type": "mcq",                 // mcq | assertion-reason | short | long | case
          "source": "CBSE 2023",         // practice sets only; see "Sources" below
          "question": "Rich text",
          "options": ["…", "…", "…", "…"],   // mcq and assertion-reason only: exactly 4, in order (A)–(D), without the letter
          "figure": "figs/q01.svg",      // optional: a figure that belongs to the question
          "parts": [                     // optional: sub-questions, e.g. a case study
            { "label": "(i)", "text": "Rich text", "marks": 1 },
            { "label": "(iii)(a)", "text": "Rich text", "marks": 2 },
            { "label": "(iii)(b)", "text": "Rich text", "marks": 2, "alt": true }   // "alt": an OR-choice for the part before it
          ],
          "solution": {
            "answer": "(A) reflexive, but neither symmetric nor transitive",   // the final answer on one line
            "concept": "Rich text",      // optional: the one formula / definition / theorem this question runs on
            "steps": [                   // single-part questions
              { "do": "Rich text", "math": "LaTeX", "why": "Rich text", "marks": 0.5, "figure": "figs/q01-sol.svg" }
            ],
            "parts": [                   // multi-part questions use this INSTEAD of "steps"; labels match question.parts
              { "label": "(i)", "steps": [ /* … */ ], "answer": "Rich text" },
              { "label": "(iii)(b)", "alt": true, "steps": [ /* … */ ], "answer": "Rich text" }
            ],
            "figure": "figs/q01-graph.svg",   // optional: a figure for the whole solution (graph, shaded region…)
            "mistake": "Rich text"       // optional: the one mistake students most often make here
          }
        }
      ]
    }
  ]
}
```

In a step only `do` is required. `math`, `why`, `marks` and `figure` are optional.

## Rich text and math

- Rich text is a plain string. Inline math goes in `$…$`. Bold is `**…**`. No HTML, no Markdown lists, no line breaks.
- `math` is display LaTeX with no `$` around it. For a chain of equalities use
  `\begin{aligned} a &= b \\ &= c \end{aligned}`. Keep it to four lines or fewer per step — a longer chain is two steps.
- Only KaTeX-supported LaTeX. Use `\dfrac` in display math, `bmatrix` for matrices, `vmatrix` for determinants,
  `\vec{a}`, `\hat{i}`, `\displaystyle\int`, `\text{…}` for words inside math. No `align`, `\tag`, `\label`, `\require`.
- **JSON escaping:** every LaTeX backslash is written twice in the file (`"\\dfrac{a}{b}"`, and a row break `\\` is `"\\\\"`).
  A single backslash silently turns `\frac`, `\theta`, `\beta`, `\neq`, `\right` into control characters; the validator rejects those.

## How a solution is written

The reader is a Class 12 student revising for an exam. They should be able to copy the solution into an answer sheet
and get full marks from a CBSE examiner.

1. **One step is one line of working.** `do` says what is being done in plain words (aim for 15 words or fewer); `math` shows it.
2. **No paragraphs anywhere.** If a step needs two sentences, it is two steps.
3. **Simple words.** "Put $x = 2$", "Cross-multiply", "Differentiate both sides w.r.t. $x$". No jargon the textbook does not use.
4. **Write what earns marks.** State the formula, definition or property before using it. Show each line an examiner
   looks for. Do not skip algebra that a student could get wrong; do not pad with lines that carry no content.
5. **Step marks follow CBSE marking schemes.** Marks sit on the steps that are value points, in halves and ones
   (`0.5`, `1`, `1.5`, …), and add up exactly to the question's marks. Typical splits: each property of a relation is a
   value point; "one-one" and "onto" are separate value points; formula ½, substitution ½, simplification, final answer ½–1;
   in an LPP the constraints, the graph, the corner-point table and the conclusion are separate value points.
   In a 1-mark MCQ the single mark sits on the step that settles the option; the other steps carry none.
6. **End with the result.** The last step states the conclusion ("Hence $R$ is an equivalence relation", "Required area $= \dfrac{9}{2}$ sq. units"),
   with units where they apply. `answer` repeats that result on one line. For an MCQ `answer` is the letter and the value: `(B) $24$`.
7. **Assertion–Reason:** one step for whether A is true, one for whether R is true, one for whether R explains A, then the option.
8. **`why` is for the non-obvious only** — a short reason (12 words or fewer) such as "$\sin^{-1}$ has range $[-\tfrac{\pi}{2}, \tfrac{\pi}{2}]$".
9. **`concept`** is one line: the key formula or idea. **`mistake`** is one line: the trap students fall into.
10. **Case study / multi-part:** solve every part under `solution.parts`, including both sides of an OR choice.
    The OR alternative carries `"alt": true` and its marks are not counted twice.

## Figures

- Add a figure wherever a board answer is expected to have one — area under curves, LPP feasible regions, the geometry
  of an optimisation problem — and wherever the question itself comes with one.
- SVG, transparent background, about 460 px wide, accurate (drawn from the real functions, to scale), text at least 11 px.
  Ink `#1f2937`, shaded region `#93c5fd` at 45% opacity, a second accent `#ef4444` if needed. Label axes, curves, key points and the region.
- Generate with matplotlib; keep the script as `content/chNN/figs/make_figs.py` so figures can be regenerated.

## Sources (practice sets)

- `source` says where a question comes from. Use an exact tag such as `CBSE 2023`, `CBSE SQP 2024-25`, `NCERT Ex 5.3 Q7`,
  `NCERT Exemplar` only when you have confirmed it against a source you opened. Otherwise write `PYQ-style` or `Board-pattern`.
  Never guess a year.
