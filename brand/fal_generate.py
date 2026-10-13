#!/usr/bin/env python3
"""Generate Red Pencil assets through FAL's queue API.

Reads the key from the FAL_KEY environment variable (never put it in a file).

Examples
--------
Still (prompt from a file; the style anchor is prepended automatically):

    python3 brand/fal_generate.py still \
        --model fal-ai/flux-2-pro \
        --prompt "a single red pencil, sharpened, lying diagonally on cream paper" \
        --size 1536x1152 --n 4 --out brand/generated

Image-to-video with Seedance (the image must be reachable by URL, e.g. a raw GitHub link):

    python3 brand/fal_generate.py video \
        --model fal-ai/bytedance/seedance/v1/pro/image-to-video \
        --image-url https://example.org/cat.png \
        --prompt "the sleeping cat's tail lifts, flicks once and settles" \
        --out brand/generated

Pass --raw to send the prompt exactly as written (no style anchor, no negative prompt).
Verify model ids on fal.ai/models; they change between versions.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

QUEUE = "https://queue.fal.run"

STYLE_ANCHOR = (
    "Editorial pen-and-ink spot illustration, confident single-weight black ink line "
    "(no variation in line thickness), minimal cross-hatching, flat fill the colour of "
    "warm cream paper (#F3EEE4), exactly one spot colour: vermilion red (#B4301E) on a "
    "single small element, everything else black line on cream, generous empty paper "
    "around the subject, slight risograph grain, subject isolated, no background scene, "
    "no text, no letters, no logo, no frame, no watermark. Subject: "
)
NEGATIVE = (
    "3D render, Pixar, Disney, glossy, plastic, gradient, bokeh, photoreal, neon, "
    "blue-purple glow, robot with a face, speech bubble, stock illustration, sticker, "
    "thick outline, text, typography, watermark, frame, border, busy background"
)
MOTION_ANCHOR = (
    "Pen-and-ink line drawing on cream paper, single black line, one red element. "
    "Static camera, no pan, no zoom, no orbit. Paper grain does not move; ink lines stay "
    "crisp with no flicker. Flat lighting. "
)


def headers() -> dict[str, str]:
    key = os.environ.get("FAL_KEY")
    if not key:
        sys.exit("FAL_KEY is not set in the environment.")
    return {"Authorization": f"Key {key}", "Content-Type": "application/json"}


def submit_and_wait(model: str, payload: dict, poll: float = 3.0, timeout: float = 900.0) -> dict:
    r = requests.post(f"{QUEUE}/{model}", headers=headers(), json=payload, timeout=60)
    r.raise_for_status()
    job = r.json()
    status_url, response_url = job["status_url"], job["response_url"]
    print(f"queued {job.get('request_id')}", file=sys.stderr)
    started = time.time()
    while True:
        s = requests.get(status_url, headers=headers(), params={"logs": "1"}, timeout=60).json()
        state = s.get("status")
        if state == "COMPLETED":
            break
        if state in {"FAILED", "CANCELLED"}:
            sys.exit(f"job {state}: {json.dumps(s, indent=2)}")
        if time.time() - started > timeout:
            sys.exit("timed out waiting for FAL")
        time.sleep(poll)
    return requests.get(response_url, headers=headers(), timeout=60).json()


def download_all(result: dict, out: Path, stem: str) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    items = []
    for key in ("images", "video", "videos", "image"):
        v = result.get(key)
        if isinstance(v, list):
            items += v
        elif isinstance(v, dict):
            items.append(v)
    for i, item in enumerate(items):
        url = item.get("url")
        if not url:
            continue
        ext = Path(url.split("?")[0]).suffix or (".mp4" if "video" in item.get("content_type", "") else ".png")
        path = out / f"{stem}-{i + 1}{ext}"
        with requests.get(url, stream=True, timeout=300) as resp:
            resp.raise_for_status()
            with open(path, "wb") as fh:
                for chunk in resp.iter_content(1 << 16):
                    fh.write(chunk)
        files.append(path)
        print(f"saved {path}")
    (out / f"{stem}.json").write_text(json.dumps(result, indent=2))
    return files


def cmd_still(a: argparse.Namespace) -> None:
    w, h = (int(x) for x in a.size.lower().split("x"))
    prompt = a.prompt if a.raw else STYLE_ANCHOR + a.prompt
    payload: dict = {
        "prompt": prompt,
        "image_size": {"width": w, "height": h},
        "num_images": a.n,
        "output_format": "png",
    }
    if not a.raw:
        payload["negative_prompt"] = NEGATIVE
    if a.seed is not None:
        payload["seed"] = a.seed
    if a.guidance is not None:
        payload["guidance_scale"] = a.guidance
    if a.image_url:
        payload["image_urls"] = [a.image_url]
    download_all(submit_and_wait(a.model, payload), Path(a.out), a.stem)


def cmd_video(a: argparse.Namespace) -> None:
    prompt = a.prompt if a.raw else MOTION_ANCHOR + a.prompt
    payload: dict = {
        "prompt": prompt,
        "image_url": a.image_url,
        "duration": str(a.seconds),
        "resolution": a.resolution,
        "camera_fixed": True,
    }
    if a.end_image_url:
        payload["end_image_url"] = a.end_image_url
    if a.seed is not None:
        payload["seed"] = a.seed
    download_all(submit_and_wait(a.model, payload), Path(a.out), a.stem)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("still", help="text-to-image (optionally with a reference image)")
    s.add_argument("--model", default="fal-ai/flux-2-pro")
    s.add_argument("--prompt", required=True)
    s.add_argument("--size", default="1536x1152", help="WIDTHxHEIGHT, multiples of 16")
    s.add_argument("--n", type=int, default=4)
    s.add_argument("--seed", type=int)
    s.add_argument("--guidance", type=float)
    s.add_argument("--image-url", help="reference image (Nano Banana / edit endpoints)")
    s.add_argument("--raw", action="store_true")
    s.add_argument("--out", default="brand/generated")
    s.add_argument("--stem", default=time.strftime("still-%Y%m%d-%H%M%S"))
    s.set_defaults(fn=cmd_still)

    v = sub.add_parser("video", help="image-to-video with Seedance")
    v.add_argument("--model", default="fal-ai/bytedance/seedance/v1/pro/image-to-video")
    v.add_argument("--prompt", required=True)
    v.add_argument("--image-url", required=True)
    v.add_argument("--end-image-url", help="pass the start image here to force a loop, if the endpoint supports it")
    v.add_argument("--seconds", type=int, default=5)
    v.add_argument("--resolution", default="720p")
    v.add_argument("--seed", type=int)
    v.add_argument("--raw", action="store_true")
    v.add_argument("--out", default="brand/generated")
    v.add_argument("--stem", default=time.strftime("video-%Y%m%d-%H%M%S"))
    v.set_defaults(fn=cmd_video)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
