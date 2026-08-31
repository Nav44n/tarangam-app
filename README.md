# Tarangam — KTU Notes

Interactive study notes for the KTU 2024 scheme. Currently covers **S5 CSE — Machine Learning (PCCST503)**, all four modules, broken down topic by topic. Built to grow into every subject and every year later — the file layout below is designed for that.

## Run it

No build step, no install. From this folder:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in a browser. (Any static server works — `npx serve`, VS Code's Live Server, etc.)

## What's here

```
ml-app/
├─ index.html          shell: sidebar, topbar, settings modal
├─ style.css            design system — dark / light / reading themes
├─ app.js                all interactivity: nav, accordions, quizzes, theming, progress
├─ content/
│  └─ ml.js              ALL Machine Learning content lives here, as data
├─ manim_scripts/
│  └─ m1_mle_hill_climb.py   one worked example script — template for the rest
└─ assets/videos/        rendered .mp4s go here (see below)
```

## Features already built

- **Topic-by-topic breakdown** — Module → smallest topic, 30 topics across the 4 modules, each its own self-contained unit (theory, formula, worked example, quiz).
- **Worked problems** wherever the syllabus has a computational method (MLE, least-squares, entropy/information gain, k-NN distance, k-means iterations, confusion-matrix metrics, PCA variance, perceptron update, etc.) — not just theory.
- **Dropdown / accordion sections** for extra depth (edge cases, derivation notes, "why does this work") so the main page stays uncluttered.
- **Self-check quizzes** on every topic — instant right/wrong feedback, an explanation on every answer, running score, saved locally.
- **Manim video slots** on topics where an animation adds real value — currently placeholders with captions describing what the clip would show, wired to auto-play once a matching `.mp4` exists (see below).
- **Three appearance modes** — dark, light, and a warm high-contrast "reading" mode — plus adjustable text size, in a proper Settings screen.
- **Progress tracking** — sidebar shows topics visited and quiz scores, stored in the browser (`localStorage`), with a one-click reset.
- **MathJax** for all formulas — no screenshots of equations.
- Responsive down to a phone screen; collapsible sidebar.

## Adding real Manim videos

Each topic with a `video` entry in `content/ml.js` points at a script path, e.g. `manim_scripts/m1_mle_hill_climb.py`. To make a clip play in-app instead of showing the caption placeholder:

1. Render it: `manim -pqh manim_scripts/m1_mle_hill_climb.py MLEHillClimb`
2. Save the output as `assets/videos/m1_mle_hill_climb.mp4`
3. In `app.js` → `renderVideo()`, point the `<video>` `src` at that path (one line — currently left as a click-to-reveal placeholder since no clips are rendered yet).

Only one script is written so far, as a template. The other 9 video slots in `content/ml.js` have a `script` path and caption ready — writing the matching `.py` for each is the remaining work, following the same pattern (Axes / plot / animate).

## Adding a new subject

Content is fully decoupled from the app shell. To add, say, DBMS:

1. Create `content/dbms.js` following the exact shape of `content/ml.js` (`window.SUBJECTS.dbms = { name, code, modules: [...] }`).
2. Add a `<script src="content/dbms.js">` tag in `index.html`.
3. In `app.js`, the `SUBJECT` constant currently hardcodes `window.SUBJECTS.ml` — swap this for a subject switcher once more than one subject exists (the sidebar already has a `subject-switch` div reserved for this).

## Adding a new year

The sidebar's "1st & 2nd" / "4th" pills are present but locked (`data-locked`) — intentionally, since only 3rd year has content right now. Wire them up the same way as subjects once that content exists.

## Design notes

Palette and type were chosen deliberately for this subject (a technical, formula-heavy set of notes meant for focused reading), not the default AI-generated look — see the "Restraint and self-critique" section of the brief this was built against. Space Grotesk (display) + Source Serif 4 (body) + IBM Plex Mono (data/labels); a cobalt/amber accent pair rather than the usual cream-and-terracotta combo; module numbers used as real navigation info, not decoration.
