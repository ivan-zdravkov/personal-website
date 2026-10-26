#!/usr/bin/env python3
"""Draw the link-preview card for zdravkov.dev/podai-globata and point the page at it.

  python3 _tools/podai-globata-preview.py [--font PATH]

Writes podai-globata/preview.png (1200x630, GitHub-style card with the Bulgarian В27 "no stopping" sign) and sets
og:image in podai-globata/index.html to preview.png?v=<content hash>, so Facebook and messengers fetch the new image
instead of a cached one. Then commit, push, and press "Scrape Again" in Facebook's Sharing Debugger.

Needs Pillow and a variable Noto Sans (Cyrillic + weight axis). This folder starts with "_", so GitHub Pages
(Jekyll) doesn't publish it.
"""
import argparse
import hashlib
import io
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "podai-globata" / "preview.png"
PAGE = ROOT / "podai-globata" / "index.html"
W, H, S = 1200, 630, 2  # draw at 2x, downscale for smooth edges
FG, MUTED, BORDER = "#1f2328", "#59636e", "#d1d9e0"
RED, BLUE = "#d62612", "#1f5fbf"

TITLE = "Подай глобата"
REPO = "ivan-zdravkov/ivan-the-terminal · civic"
TAGLINE = "Снимате неправилно паркирана кола, а Claude пише официалния сигнал до правилната институция."
STATS = [("1+", "снимки"), ("1 мин", "до сигнала"), ("0 €", "безплатно"), ("MIT", "отворен код")]
CAPTION = "Skill за Claude"


def font(path, size, weight):
    f = ImageFont.truetype(path, size * S)
    f.set_variation_by_axes([weight])
    return f


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def disc(d, cx, cy, r, fill):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)


def sign(im, cx, cy, r):
    """В27: white rim, red ring, white line, blue disc, red X with white edges (as painted on Bulgarian signs)."""
    d = ImageDraw.Draw(im)
    disc(d, cx, cy, r, "#c4ccd4")                      # hairline so the white rim shows on a white card
    disc(d, cx, cy, r - int(1.5 * S), "white")         # outer white rim
    rr = int(r * 0.93)
    disc(d, cx, cy, rr, RED)                           # red ring
    ri, edge = int(r * 0.72), int(r * 0.035)
    disc(d, cx, cy, ri + edge, "white")                # white line between ring and disc
    disc(d, cx, cy, ri, BLUE)                          # blue disc
    clip = Image.new("L", im.size, 0)                  # the X spans the disc and its white line, joining the ring
    rc = ri + edge
    ImageDraw.Draw(clip).ellipse((cx - rc, cy - rc, cx + rc, cy + rc), fill=255)
    k, w = rr * 0.7071, int(r * 0.19)
    for colour, width in (("white", w + 2 * edge), (RED, w)):  # white edges first, then the red bars
        mask = Image.new("L", im.size, 0)
        md = ImageDraw.Draw(mask)
        md.line((cx - k, cy - k, cx + k, cy + k), fill=255, width=width)
        md.line((cx - k, cy + k, cx + k, cy - k), fill=255, width=width)
        im.paste(colour, (0, 0), ImageChops.multiply(mask, clip))


def draw(font_path):
    im = Image.new("RGB", (W * S, H * S), "white")
    d = ImageDraw.Draw(im)
    x = 80 * S
    d.text((x, 70 * S), REPO, font=font(font_path, 30, 400), fill=MUTED)
    d.text((x, 118 * S), TITLE, font=font(font_path, 92, 700), fill=FG)
    body = font(font_path, 36, 400)
    y = 262 * S
    for line in wrap(d, TAGLINE, body, 700 * S):
        d.text((x, y), line, font=body, fill=MUTED)
        y += 52 * S
    sx = x
    for value, label in STATS:  # GitHub-style stats row: value over label
        d.text((sx, 430 * S), value, font=font(font_path, 36, 700), fill=FG)
        d.text((sx, 478 * S), label, font=font(font_path, 24, 400), fill=MUTED)
        sx += 190 * S

    cx, cy, r = 990 * S, 250 * S, 140 * S
    sign(im, cx, cy, r)
    d = ImageDraw.Draw(im)
    d.text((cx, cy + r + 38 * S), CAPTION, font=font(font_path, 26, 600), fill=MUTED, anchor="mm")

    bar = H * S - 22 * S  # like GitHub's language bar, in the Bulgarian tricolour
    d.rectangle((0, bar, W * S * 0.34, H * S), fill="#e9ecef")
    d.rectangle((W * S * 0.34, bar, W * S * 0.67, H * S), fill="#00966e")
    d.rectangle((W * S * 0.67, bar, W * S, H * S), fill=RED)
    d.line((0, bar, W * S, bar), fill=BORDER, width=S)
    return im.resize((W, H), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default="/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf")
    args = ap.parse_args()
    buf = io.BytesIO()
    draw(args.font).save(buf, "PNG", optimize=True)
    OUT.write_bytes(buf.getvalue())
    version = hashlib.sha256(buf.getvalue()).hexdigest()[:8]
    html = PAGE.read_text(encoding="utf-8")
    new = re.sub(r"(podai-globata/preview\.png)(\?v=[\w-]+)?", rf"\1?v={version}", html)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} written; og:image -> preview.png?v={version}")


if __name__ == "__main__":
    main()
