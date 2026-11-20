#!/usr/bin/env python3
"""Build the GTA 6 meme 'THE RECEIPT' (1200x1200, square for X).

Scene: the make.fun ghost — cut out of the real press-kit mark
(mark-1024.png, white ghost, thick black outline, sparkle eyes, magenta
coin with a white star, round little hand) — stands BEHIND the counter of
Leonida Mart in Vice City as the cashier. In front of it, a big white
receipt itemises the 13-year wait since GTA V. All text is drawn with PIL
so every word is spelled exactly and stays readable when the judge shrinks
the picture to 480x480.
"""
from PIL import Image, ImageDraw, ImageFont
import math, random

W = H = 1200
GHOST = "/tmp/ghost-cutout.png"
OUT = "meme.png"

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---- background: Vice City dusk gradient + stars + neon glow ----
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
top = (26, 8, 52)       # deep purple night
mid = (94, 16, 96)      # magenta dusk
bot = (168, 18, 110)    # neon pink horizon
for y in range(H):
    t = y / H
    if t < 0.55:
        k = t / 0.55
        c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
    else:
        k = (t - 0.55) / 0.45
        c = tuple(int(mid[i] + (bot[i] - mid[i]) * k) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

random.seed(6)
for _ in range(90):
    x, y = random.randint(0, W - 1), random.randint(0, 420)
    r = random.choice([1, 1, 2])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))

# ---- store sign ----
def text_c(draw, cx, y, s, f, fill, stroke=0, stroke_fill=None):
    w = draw.textlength(s, font=f)
    draw.text((cx - w / 2, y), s, font=f, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill or (0, 0, 0))
    return w

text_c(d, 600, 36, "★ LEONIDA MART ★", font(SANS, 84), (255, 255, 255),
       stroke=3, stroke_fill=(20, 4, 40))
text_c(d, 600, 132, "VICE CITY  •  OPEN LATE  •  EST. 2013", font(SANS, 34),
       (255, 214, 64))

# ---- ghost cashier behind the counter ----
ghost = Image.open(GHOST).convert("RGBA")
ghost = ghost.resize((560, int(560 * ghost.height / ghost.width)),
                     Image.LANCZOS)
img.paste(ghost, (320, 180), ghost)
d = ImageDraw.Draw(img)

# ---- counter ----
d.rectangle([0, 700, W, H], fill=(38, 8, 66))
d.rectangle([0, 700, W, 726], fill=(214, 0, 127))          # counter top
d.rectangle([0, 726, W, 734], fill=(255, 214, 64))

# ---- receipt (taller: each item gets its own name line + qty/price line) ----
RX0, RX1, RY0 = 130, 1070, 520
receipt_h = 640
ry1 = RY0 + receipt_h
d.rounded_rectangle([RX0, RY0, RX1, ry1 + 14], radius=6, fill=(255, 255, 255))
# zigzag bottom edge
zz = []
x = RX0
while x < RX1:
    zz.append((x, ry1 + 14))
    zz.append((x + 14, ry1 + 30))
    x += 28
zz.append((RX1, ry1 + 14))
d.polygon(zz, fill=(255, 255, 255))
d.rectangle([RX0, ry1 + 2, RX1, ry1 + 14], fill=(255, 255, 255))

y = RY0 + 14
text_c(d, 600, y, "LEONIDA MART", font(MONO, 48), (0, 0, 0))
y += 58
text_c(d, 600, y, "VICE CITY, LEONIDA", font(MONO, 28), (60, 60, 60))
y += 44
d.line([(RX0 + 30, y), (RX1 - 30, y)], fill=(0, 0, 0), width=3)
y += 18

# one item = name line, then qty left + price right on the next line
rows = [
    ("WAITING SINCE GTA V (2013)", "13 YEARS", "$0.00"),
    ("LAUNCH DELAYS", "2", "$0.00"),
    ("SICK DAYS BOOKED FOR LAUNCH WEEK", "3", "$0.00"),
    ("DOWNLOAD SIZE", "ALL OF IT", "$0.00"),
]
f_item, f_qty, f_price = font(MONO, 38), font(MONO, 36), font(MONO, 38)
for name, qty, price in rows:
    d.text((RX0 + 34, y), name, font=f_item, fill=(0, 0, 0))
    y += 42
    pw = d.textlength(price, font=f_price)
    d.text((RX0 + 34, y), qty, font=f_qty, fill=(0, 0, 0))
    d.text((RX1 - 34 - pw, y), price, font=f_price, fill=(0, 0, 0))
    y += 42

d.line([(RX0 + 30, y), (RX1 - 30, y)], fill=(0, 0, 0), width=3)
y += 14
text_c(d, 600, y, "TOTAL DUE:  $0.00", font(MONO, 50), (166, 0, 102))
y += 62
text_c(d, 600, y, "PAID BY MY AI AGENT", font(MONO, 40), (166, 0, 102))
y += 46
text_c(d, 600, y, "ON MAKE.FUN", font(MONO, 40), (166, 0, 102))

img.save(OUT)
print("saved", OUT, img.size)

# judge-view check: shrink to 480x480 exactly like the judge sees it
small = img.resize((480, 480), Image.LANCZOS)
small.save("/tmp/meme-480.png")
print("saved /tmp/meme-480.png")
