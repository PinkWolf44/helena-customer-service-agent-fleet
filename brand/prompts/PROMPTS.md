# Red Pencil — prompt pack for FAL

Every still prompt begins with the style anchor from `../STYLE.md` §5. It is repeated here so
this file is copy-paste complete. Replace the `[SUBJECT]` line only; leave the rest alone.

## Style anchor

```
Editorial pen-and-ink spot illustration, confident single-weight black ink line
(no variation in line thickness), minimal cross-hatching, flat fill the colour of
warm cream paper (#F3EEE4), exactly one spot colour: vermilion red (#B4301E) on a
single small element, everything else black line on cream, generous empty paper
around the subject, slight risograph grain, subject isolated, no background scene,
no text, no letters, no logo, no frame, no watermark.
```

Negative (FLUX / Seedream / Recraft accept one; Nano Banana does not, fold it into the prose):

```
3D render, Pixar, Disney, glossy, plastic, gradient, bokeh, photoreal, neon,
blue-purple glow, robot with a face, speech bubble, stock illustration, sticker,
thick outline, text, typography, watermark, frame, border, busy background
```

---

## A. The cat (character sheet)

Use with the browser cat PNG (`banner/out/linkedin-banner.png`, cropped to the cat) as the
reference image on Nano Banana Pro, or standalone on FLUX.

```
[STYLE ANCHOR]
Subject: a small domestic cat asleep in a loaf pose, seen from the side, head to the
right resting on its front paws, eyes closed as two short curved lines, three short
curved stripes on its back, a few whiskers, a tiny red nose as the only red element.
Drawn with the economy of a magazine spot illustration: about a dozen strokes.
Lying on the edge of a sheet of paper. Nothing else in frame.
```

Variants (change the second sentence only):
- `...asleep on a short stack of index cards, one card slightly askew.`
- `...asleep across the open gutter of a manuscript, one paw over a line of handwriting (handwriting is illegible squiggles, not letters).`
- `...asleep beside an ink bottle and a red pencil; the pencil is the red element, the nose is black here.`

## B. Objects (post illustrations)

```
[STYLE ANCHOR]
Subject: a single red pencil, sharpened, lying diagonally on cream paper, its shadow
drawn as a few hatched lines; the pencil body is the one red element.
```

```
[STYLE ANCHOR]
Subject: a Jacquard loom punch card, slightly curled, holes drawn as a neat grid of
small rectangles, one hole filled red.
```

```
[STYLE ANCHOR]
Subject: a card-catalogue drawer pulled halfway open, index cards fanned inside,
one card tab marked with a red dot.
```

```
[STYLE ANCHOR]
Subject: a magnifying glass resting over a line of illegible handwriting (squiggles,
not letters); the glass rim is black ink, a single red caret mark sits under the line.
```

```
[STYLE ANCHOR]
Subject: a letterpress composing stick holding a row of metal type sorts, seen at a
slight angle; one sort is red.
```

```
[STYLE ANCHOR]
Subject: a short loop of paper tape with punched holes, curling like a ribbon on
cream paper; one hole is red.
```

## C. Settings per endpoint

| Endpoint | Size | Guidance / steps | Notes |
|---|---|---|---|
| `fal-ai/flux-2-pro` | 1536×1536 or 1536×1152 | guidance 3.5, steps 28 | `safety_tolerance` default; fix `seed` for a series |
| `fal-ai/flux-pro/v1.1-ultra` | aspect 1:1 or 4:3 | raw: false | strongest line discipline; no steps control |
| `fal-ai/nano-banana-pro` | 1K–2K | n/a | pass `image_urls: [cat reference]`; say "keep this exact cat" |
| `fal-ai/bytedance/seedream/v4/text-to-image` | 2048×2048 | default | use for anything you will animate |
| `fal-ai/recraft/v3/text-to-image` | 1024×1024 | style `vector_illustration/line_art` | gives clean vectors; red may need colour-picking in the editor |

Verify each id on fal.ai/models before a run; names shift between versions.

---

## D. Seedance (image-to-video)

Always image-to-video from a still in this style. Static camera. One action. 5 seconds.
Compose the typography separately (`banner/render.js --animate`).

**Cat, tail flick (loop):**
```
Pen-and-ink line drawing on cream paper, single black line, one red element.
The sleeping cat stays perfectly still except for its tail, which lifts, flicks once
to the left and settles back exactly where it started. Eyes stay closed. Static camera,
no pan, no zoom, no orbit. Paper grain does not move; ink lines stay crisp with no
flicker or boiling. Flat lighting, no shadows appearing. 5 seconds, ends on the start pose.
```

**Cat, ear twitch:**
```
Pen-and-ink line drawing on cream paper, single black line, one red element.
The sleeping cat is motionless; its left ear twitches twice, quickly, then rests.
Static camera, no pan, no zoom. Ink stays crisp, paper grain static, nothing else
in the frame changes. 4 seconds.
```

**Red pencil draws a strike (for a post where the type is composited on top):**
```
Pen-and-ink line drawing on cream paper. A red pencil enters from the right, lies
down on the paper and draws a single straight red line from left to right across
the middle of the empty frame, then lifts away. Static camera, flat lighting,
the line it leaves stays. No text appears. 5 seconds.
```

**Index card slides in:**
```
Pen-and-ink line drawing on cream paper. A blank index card slides in from the
bottom edge and stops in the lower third, slightly rotated, with a small red dot in
its corner. Static camera, no zoom. 4 seconds, holds on the final frame.
```

Seedance prompt rules that matter in practice:
1. Name the camera as static *and* list the moves you do not want. It otherwise adds a slow push-in.
2. One verb per shot. Two verbs become a different second shot.
3. Say what stays still (grain, lines, eyes). Unspecified things wander.
4. If the endpoint accepts a `last_frame` or `end_image`, pass the start image to force a loop.
5. 720p is enough for a feed; upscale with the same pipeline that handles the type.
