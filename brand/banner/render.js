// Renders banner.html to PNG stills and, with --animate, to an MP4 + GIF write-on loop.
//
//   node render.js                 -> linkedin-banner.png (1584x396 @2x), x-header.png (1500x500 @2x)
//   node render.js --animate       -> also linkedin-banner-animated.mp4 / .gif (6 s, 30 fps)
//
// Needs Playwright (Chromium) and ffmpeg on PATH or FFMPEG=/path/to/ffmpeg.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');

const HERE = __dirname;
const OUT = path.join(HERE, 'out');
const SIZES = [
  { name: 'linkedin-banner', w: 1584, h: 396 },
  { name: 'x-header', w: 1500, h: 500 },
];
const FPS = 30, SECONDS = 6;

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const url = 'file://' + path.join(HERE, 'banner.html');

  for (const s of SIZES) {
    const page = await browser.newPage({ viewport: { width: s.w, height: s.h }, deviceScaleFactor: 2 });
    await page.goto(`${url}?w=${s.w}&h=${s.h}`);
    await page.waitForFunction(() => window.__ready === true);
    await page.screenshot({ path: path.join(OUT, `${s.name}.png`) });
    await page.close();
    console.log('wrote', `${s.name}.png`);
  }

  if (process.argv.includes('--animate')) {
    const s = SIZES[0];
    const frames = path.join(OUT, 'frames');
    fs.rmSync(frames, { recursive: true, force: true });
    fs.mkdirSync(frames);
    const page = await browser.newPage({ viewport: { width: s.w, height: s.h }, deviceScaleFactor: 1 });
    await page.goto(`${url}?w=${s.w}&h=${s.h}&animate=1`);
    await page.waitForFunction(() => window.__ready === true);
    // Pause every CSS animation and scrub it by hand, one frame at a time.
    await page.evaluate(() => document.getAnimations().forEach(a => a.pause()));
    const n = FPS * SECONDS;
    for (let i = 0; i < n; i++) {
      const t = (i / FPS) * 1000;
      await page.evaluate(ms => document.getAnimations().forEach(a => { a.currentTime = ms; }), t);
      await page.screenshot({ path: path.join(frames, `f${String(i).padStart(4, '0')}.png`) });
    }
    await page.close();
    const ffmpeg = process.env.FFMPEG || 'ffmpeg';
    const seq = path.join(frames, 'f%04d.png');
    execFileSync(ffmpeg, ['-y', '-framerate', String(FPS), '-i', seq, '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
      '-crf', '18', '-movflags', '+faststart', path.join(OUT, `${s.name}-animated.mp4`)], { stdio: 'inherit' });
    execFileSync(ffmpeg, ['-y', '-framerate', String(FPS), '-i', seq, '-vf',
      'fps=15,scale=1200:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=bayer:bayer_scale=4',
      '-loop', '0', path.join(OUT, `${s.name}-animated.gif`)], { stdio: 'inherit' });
    fs.rmSync(frames, { recursive: true, force: true });
    console.log('wrote', `${s.name}-animated.mp4`, `${s.name}-animated.gif`);
  }
  await browser.close();
}
main().catch(e => { console.error(e); process.exit(1); });
