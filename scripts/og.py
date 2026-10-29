#!/usr/bin/env python3
"""Generate a 1200x630 blog share image in the Altos style.

Usage: python3 scripts/og.py LABEL "Post title" output-filename.png [font_px]
Example: python3 scripts/og.py GUIDE "My Post Title" blog-my-post-og.png 50
Writes to assets/. Downloads the Sora font (OFL, Google Fonts) to scripts/.fonts/ on first run.
"""
import os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, ".fonts"); os.makedirs(FONT_DIR, exist_ok=True)
FONT = os.path.join(FONT_DIR, "Sora-var.ttf")
if not os.path.exists(FONT):
    urllib.request.urlretrieve("https://github.com/google/fonts/raw/main/ofl/sora/Sora%5Bwght%5D.ttf", FONT)
OUT = os.path.join(HERE, "..", "assets")

label, title, fname = sys.argv[1], sys.argv[2], sys.argv[3]
size = int(sys.argv[4]) if len(sys.argv) > 4 else 50
NS, ND = (27, 58, 91, 255), (15, 36, 56, 255)
TEAL, WHITE = (95, 191, 174, 255), (255, 255, 255, 255)

def sora(px, w=800):
    f = ImageFont.truetype(FONT, int(px))
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f

def stroke(d, pts, c, w):
    w = int(w)
    for i in range(len(pts) - 1): d.line([pts[i], pts[i + 1]], fill=c, width=w)
    r = w / 2
    for (x, y) in pts: d.ellipse([x - r, y - r, x + r, y + r], fill=c)

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = word
    if cur: lines.append(cur)
    return lines

SS = 2; W, H = 1200 * SS, 630 * SS
grad = Image.new("L", (1, H))
for y in range(H): grad.putpixel((0, y), int(255 * y / (H - 1)))
img = Image.composite(Image.new("RGBA", (W, H), ND), Image.new("RGBA", (W, H), NS), grad.resize((W, H))).convert("RGBA")

chev = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(chev); cx, span = W * 0.84, H * 0.8
for i, col in enumerate([TEAL, WHITE, TEAL]):
    o = i * H * 0.24
    stroke(cd, [(cx - span, H * 1.02 + o), (cx, H * 0.12 + o), (cx + span, H * 1.02 + o)], col, H * 0.028)
chev.putalpha(chev.getchannel("A").point(lambda a: int(a * 0.08))); img.alpha_composite(chev)

d = ImageDraw.Draw(img); m = int(H * 0.12); u = SS * 0.62
P = lambda x, y: (m + x * u, m + y * u)
stroke(d, [P(6, 52), P(28, 8), P(50, 52)], WHITE, 9 * u)
stroke(d, [P(16, 45), P(28, 24), P(40, 45)], TEAL, 7.5 * u)
d.text((m + 58 * u, m + 18 * u), "LTOS", font=sora(30 * SS), fill=WHITE)
d.text((m + 58 * u + d.textlength("LTOS", font=sora(30 * SS)) + 16 * SS, m + 22 * u), "BLOG", font=sora(15 * SS, 600), fill=TEAL)
d.text((m, H * 0.33), label.upper(), font=sora(17 * SS, 700), fill=TEAL)
f = sora(size * SS); y = H * 0.39
for line in wrap(d, title, f, W - 2 * m):
    d.text((m, y), line, font=f, fill=WHITE); y += size * SS * 1.13
d.text((m, H - m - 24 * SS), "By Al Camasis, Founder", font=sora(20 * SS, 600), fill=(255, 255, 255, 220))
img.resize((1200, 630), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, fname), quality=92)
print("wrote assets/" + fname)
