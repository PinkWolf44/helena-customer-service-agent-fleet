# Red Pencil — visual style sheet

A house style for Helena's personal brand on LinkedIn and X. One idea, carried everywhere:
**machine text, corrected by a human hand.** The red pencil is the mark of judgment; the
cream paper is the manuscript; the cat is the only creature allowed, and it is asleep.

Built to be produced two ways at once: typography rendered in a browser (exact, cheap,
never misspelt), illustration generated through FAL image models and animated with Seedance.
Image models get the *pictures*; they never get the *words*.

---

## 1. Why this and not a Pixar robot

| The old banner | The problem | Red Pencil's answer |
|---|---|---|
| Glossy 3D robot with a heart on its chest | Every AI consultant has one; it says "AI" and nothing about *you* | The subject is *correction*, which is literally what philology and human-in-the-loop work are |
| Cute stacked three deep (robot + heart bubble + cat) | Cuteness as a substitute for a point of view | One cute thing (the cat), earned by restraint around it |
| Editorial serif headline + storybook render | Two styles that don't know each other | One style: ink line, spot red, paper. Type and picture share the same palette and the same joke |
| Model-generated typography | Soft, slightly wrong letterforms; unfixable | Real fonts, rendered by Chromium; the model only draws things that may wobble |

It performs in a feed for mechanical reasons too: a warm paper card reads as an object on both
LinkedIn-white and X-dark; one saturated red is a reliable scroll-stopper among blue gradients;
line art survives heavy compression and small thumbnails; and the "correction" device gives
every post a built-in before/after, which is what animated posts need.

## 2. Tokens

### Colour

| Role | Hex | Use |
|---|---|---|
| Paper | `#F3EEE4` | Every background. Never pure white. |
| Ink | `#1C1A17` | Headlines, line art, outlines. Never pure black. |
| Red pencil | `#B4301E` | The *only* accent. Corrections, carets, the cat's nose, the margin rule, the dots in the tag row. |
| Graphite | `#8A8279` | "Machine text": the model's output before review, captions, metadata. |
| Rule | `#D8D0C2` | Hairlines, table rules, faint guides. |

Red budget: at most 8% of any composition. If you want more red, you want a second idea, not more red.

### Type

| Role | Face | Settings |
|---|---|---|
| Headline | **Fraunces** (variable) | weight 480, `opsz` 144, `SOFT` 40, `WONK` 1, tracking −1.2%, leading 1.16 |
| Correction / insertion | Fraunces *italic* | weight 500, `SOFT` 60, `WONK` 1, always in Red pencil, 40% of headline size |
| Machine text | **IBM Plex Mono** 400 | Graphite, leading 1.95, generous |
| Labels / tag row | IBM Plex Mono 500 | uppercase, tracking 24%, 14–15 px at 1584 wide |
| Captions | IBM Plex Mono 400 | uppercase, tracking 18%, ~11.5 px, Graphite |

Fraunces is the "human" voice (warm, wonky, old-style). Plex Mono is the "machine" voice.
Never swap them: a correction is always serif italic red; machine output is always mono grey.

### The marks (vocabulary of human judgment)

| Mark | Drawn as | Meaning in the story |
|---|---|---|
| Caret `^` under the baseline | 3 px red stroke, open V | "insert here" — the human adds what was missing |
| Strike | single 2.2 px red line, 3° rise, through the x-height | "delete" — never a scribble |
| Replacement word | serif italic red above the struck word | the better word |
| `stet` + dotted underline | mono red, tiny, below | "let it stand" — the human keeps what the machine got right |
| Margin rule | 1.5 px red, 55% opacity, vertical | the edge of the manuscript page |

Use at most three marks per composition. Marks are measured from real glyph boxes
(see `banner/banner.html`), never eyeballed.

### Texture

Paper grain: fractal noise at 5–6% opacity, multiply. Enough that flat colour doesn't look
like a vector export; never enough to be "vintage".

## 3. The cat

One recurring creature. Rules:

- Ink line only, same weight as everything else (2.3 px at 1584 wide), paper-coloured fill.
- Loaf pose, eyes closed, three back stripes, whiskers, a red nose. That is the whole character.
- It never talks, never wears anything, never has a screen for a face, never looks at the viewer.
- It is near the work (asleep on the proofs, on the margin, on a stack of cards). It is not the subject.
- In motion: a tail flick or an ear twitch, once. Cats do not wave.

The browser-drawn version lives in `banner/banner.html` and is the canonical reference for
the generated versions (use it as the reference image when prompting).

## 4. Composition rules

- **Left-aligned headline, two lines, one correction.** Centred headlines are for posters; this is a manuscript.
- **Negative space is the design.** 55–65% of the canvas is empty paper.
- **Headline block starts at 19% of the width** on banners. On LinkedIn the profile photo covers the
  bottom-left corner; on X it covers the bottom-left too. Nothing important lives there.
- **The specimen** (machine text + marks) sits right, never wider than 28% of the canvas, with the
  red margin rule on its left. The cat sits on top of the specimen's top-right corner.
- **One joke per surface.** The banner's joke is "human" inserted into "AI, language & judgment".
  A post gets a different correction. Don't reuse the same specimen twice.

### Canvas sizes

| Surface | Size | Notes |
|---|---|---|
| LinkedIn banner | 1584 × 396 (export @2×) | mobile crops the sides ~10%; keep text inside the middle 80% |
| X header | 1500 × 500 (export @2×) | photo overlaps bottom-left ~ 210 × 150 |
| LinkedIn / X post, square | 1080 × 1080 | headline 3 lines, specimen below, cat bottom-right |
| LinkedIn / X post, landscape | 1200 × 675 | same grid as the banner, more leading |
| Video post | 1584 × 396 or 1200 × 675, MP4 H.264, 6 s loop | see §6 |

## 5. Prompting the image models (FAL)

The models draw objects; the browser sets type. Never ask a model for a word, a letter or a caption.

### Style anchor (paste verbatim at the start of every prompt)

```
Editorial pen-and-ink spot illustration, confident single-weight black ink line
(no variation in line thickness), minimal cross-hatching, flat fill the colour of
warm cream paper (#F3EEE4), exactly one spot colour: vermilion red (#B4301E) on a
single small element, everything else black line on cream, generous empty paper
around the subject, slight risograph grain, subject isolated, no background scene,
no text, no letters, no logo, no frame, no watermark.
```

### Negative prompt (where the endpoint takes one)

```
3D render, Pixar, Disney, glossy, plastic, gradient, bokeh, photoreal, neon,
blue-purple glow, robot with a face, speech bubble, stock illustration, sticker,
thick outline, text, typography, watermark, frame, border, busy background
```

### Which endpoint for what

| Need | Endpoint (verify the id on fal.ai/models before running) | Why |
|---|---|---|
| New spot illustration | `fal-ai/flux-2-pro` (or `fal-ai/flux-pro/v1.1-ultra`) | most obedient to "single-weight line, one spot colour"; honours custom sizes |
| Same object, new pose, same cat | `fal-ai/nano-banana-pro` with the browser cat PNG as reference | best at keeping a character consistent from a reference image |
| Still that will be animated | `fal-ai/bytedance/seedream/v4/text-to-image` | sibling of Seedance, so motion keeps the look |
| True vector / SVG output | `fal-ai/recraft/v3/text-to-image` with style `vector_illustration/line_art` | when the asset must scale or be edited |
| Text inside the image | don't. Render it in the browser and composite. | |

Settings that behave: guidance 3–4 (FLUX), 20–28 steps, seed fixed per series, 1:1 or 4:3 for
spot illustrations (crop later), 1536 px longest side. Generate 4, keep 1.

### Subject vocabulary (things that may be drawn)

Red pencil · caret · manuscript page with marginalia · index cards · card-catalogue drawer ·
Jacquard punch card (the first "program") · letterpress sort and composing stick · ink bottle ·
magnifying glass over a line of text · bookbinder's thread · reel of paper tape · the cat, asleep.

The *machine* is shown through its artefacts (punch card, paper tape, a block cursor), never as a
humanoid robot.

Ready-made prompts are in `prompts/PROMPTS.md`.

## 6. Motion (Seedance on FAL)

What Seedance is good at here, and what it is not:

- **Image-to-video from your own still.** Always start from a browser render or a Seedream/FLUX
  still in this style. Text-to-video from scratch drifts off-style in two seconds.
- **Locked-off camera.** Say it explicitly: "static camera, no pan, no zoom, no orbit". Line art
  on flat paper has no parallax to sell a camera move, and the model will invent one if asked.
- **One action per shot, 4–6 s.** "The cat's tail flicks once and settles." Not "the cat wakes,
  stretches and walks off".
- **Loop by construction:** ask for the end state to equal the start state (tail returns to rest);
  if the endpoint offers a last-frame input, pass the first frame as the last frame.
- **Keep text out of the video layer.** Animate the picture in Seedance; animate the type in the
  browser (`banner/render.js --animate` does the write-on); composite in the editor or with ffmpeg.
- **Prompt shape** that works: `[style anchor, shortened] + [subject at rest] + [one small action] +
  [camera: static] + [texture: paper grain stays still, ink lines stay crisp, no flicker]`.

Motion vocabulary: a red strike draws itself left to right · a caret is drawn in two strokes ·
a word fades in above it · the tail flicks · an ear twitches · an index card slides into frame ·
a page corner lifts and settles. Nothing bounces, nothing sparkles, nothing waves.

## 7. Anti-slop checklist

Before publishing anything in this style, every box must be ticked:

- [ ] Exactly one red element carries meaning; the rest is ink and paper.
- [ ] No gradient, no glow, no 3D, no drop shadow anywhere.
- [ ] Typography was rendered by the browser, not the model.
- [ ] Line weight is uniform across type marks, cat and illustration.
- [ ] 55%+ of the canvas is empty paper.
- [ ] The correction makes a point a reader could repeat ("the agent drafts; a human sends").
- [ ] The cat is asleep and not the subject.
- [ ] It survives a 320 px thumbnail: headline legible, red mark visible, cat recognisable.

## 8. Files

```
brand/
  STYLE.md                     this document
  prompts/PROMPTS.md           copy-paste prompts for FAL (stills and Seedance)
  fal_generate.py              CLI for FAL's queue API (reads FAL_KEY from the environment)
  banner/
    banner.html                the banner, type + marks + cat; ?w=&h=&animate=1
    render.js                  Playwright renderer: PNG stills, MP4 + GIF write-on loop
    fonts/                     Fraunces + IBM Plex Mono (Latin subsets, OFL)
    out/                       rendered deliverables
```
