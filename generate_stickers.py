"""
LINE sticker generator using Pillow.

LINE sticker specs:
  Main image: 370 x 320 px, PNG
  Tab icon:    96 x  74 px, PNG
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

STICKER_W, STICKER_H = 370, 320
TAB_W, TAB_H = 96, 74
OUT_DIR = "stickers"

YELLOW = (255, 220, 50, 255)
OUTLINE = (60, 40, 0, 255)
WHITE = (255, 255, 255, 255)
BLACK = (30, 30, 30, 255)
RED = (220, 50, 50, 255)
PINK = (255, 150, 170, 255)
BLUE = (80, 130, 220, 255)
TRANSPARENT = (0, 0, 0, 0)

OUTLINE_W = 6


def new_canvas() -> tuple[Image.Image, ImageDraw.Draw]:
    img = Image.new("RGBA", (STICKER_W, STICKER_H), TRANSPARENT)
    return img, ImageDraw.Draw(img)


def ellipse_outline(draw: ImageDraw.Draw, box, fill, outline, width):
    draw.ellipse(box, fill=outline)
    inner = [
        box[0] + width,
        box[1] + width,
        box[2] - width,
        box[3] - width,
    ]
    draw.ellipse(inner, fill=fill)


def face_base(draw: ImageDraw.Draw, cx: int, cy: int, rx: int, ry: int):
    """Draw the yellow face oval with outline."""
    box = [cx - rx, cy - ry, cx + rx, cy + ry]
    ellipse_outline(draw, box, YELLOW, OUTLINE, OUTLINE_W)


def eye(draw: ImageDraw.Draw, cx: int, cy: int, r: int = 14):
    """Simple round eye."""
    box = [cx - r, cy - r, cx + r, cy + r]
    ellipse_outline(draw, box, BLACK, WHITE, 3)


def eye_closed(draw: ImageDraw.Draw, cx: int, cy: int, r: int = 14):
    """Closed (happy squint) eye — arc line."""
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=OUTLINE, width=5)


def mouth_smile(draw: ImageDraw.Draw, cx: int, cy: int, w: int = 60, h: int = 30):
    draw.arc([cx - w, cy - h, cx + w, cy + h], 10, 170, fill=OUTLINE, width=6)


def mouth_sad(draw: ImageDraw.Draw, cx: int, cy: int, w: int = 60, h: int = 30):
    draw.arc([cx - w, cy, cx + w, cy + h * 2], 190, 350, fill=OUTLINE, width=6)


def mouth_open(draw: ImageDraw.Draw, cx: int, cy: int, w: int = 50, h: int = 40):
    draw.ellipse([cx - w, cy - h // 2, cx + w, cy + h], fill=OUTLINE)
    draw.ellipse([cx - w + 8, cy, cx + w - 8, cy + h - 6], fill=RED)


def cheek(draw: ImageDraw.Draw, cx: int, cy: int):
    draw.ellipse([cx - 22, cy - 10, cx + 22, cy + 10], fill=(*PINK[:3], 160))


# ── individual stickers ────────────────────────────────────────────────────────

def sticker_happy() -> Image.Image:
    img, draw = new_canvas()
    cx, cy = 185, 160
    face_base(draw, cx, cy, 120, 110)
    eye_closed(draw, cx - 45, cy - 20)
    eye_closed(draw, cx + 45, cy - 20)
    mouth_smile(draw, cx, cy + 20, 65, 35)
    cheek(draw, cx - 75, cy + 10)
    cheek(draw, cx + 75, cy + 10)
    return img


def sticker_sad() -> Image.Image:
    img, draw = new_canvas()
    cx, cy = 185, 160
    face_base(draw, cx, cy, 120, 110)
    # droopy eyes
    draw.arc([cx - 60, cy - 40, cx - 25, cy - 15], 20, 160, fill=OUTLINE, width=5)
    draw.arc([cx + 25, cy - 40, cx + 60, cy - 15], 20, 160, fill=OUTLINE, width=5)
    mouth_sad(draw, cx, cy + 30, 50, 25)
    # tear
    for i in range(4):
        draw.ellipse([cx - 55 + i, cy + 5 + i * 10, cx - 47 + i, cy + 14 + i * 10], fill=BLUE)
    return img


def sticker_love() -> Image.Image:
    img, draw = new_canvas()
    cx, cy = 185, 160
    face_base(draw, cx, cy, 120, 110)

    def heart(x, y, size=22):
        # crude heart via two circles + polygon
        r = size // 2
        draw.ellipse([x - r, y - r, x + r - 1, y + r - 1], fill=RED)
        draw.ellipse([x, y - r, x + size, y + r - 1], fill=RED)
        draw.polygon([(x - r, y + r // 2), (x + size // 2, y + size), (x + size + r, y + r // 2)], fill=RED)

    heart(cx - 62, cy - 38)
    heart(cx + 22, cy - 38)
    mouth_smile(draw, cx, cy + 15, 65, 35)
    cheek(draw, cx - 75, cy + 10)
    cheek(draw, cx + 75, cy + 10)
    return img


def sticker_angry() -> Image.Image:
    img, draw = new_canvas()
    cx, cy = 185, 160
    face_base(draw, cx, cy, 120, 110)
    # angled brows
    draw.line([cx - 60, cy - 50, cx - 25, cy - 35], fill=OUTLINE, width=7)
    draw.line([cx + 25, cy - 35, cx + 60, cy - 50], fill=OUTLINE, width=7)
    eye(draw, cx - 42, cy - 15, 16)
    eye(draw, cx + 42, cy - 15, 16)
    # small angry mouth
    draw.arc([cx - 40, cy + 30, cx + 40, cy + 60], 200, 340, fill=OUTLINE, width=6)
    # vein symbol
    draw.line([cx + 70, cy - 70, cx + 85, cy - 80], fill=RED, width=4)
    draw.line([cx + 85, cy - 80, cx + 95, cy - 65], fill=RED, width=4)
    return img


def sticker_sleeping() -> Image.Image:
    img, draw = new_canvas()
    cx, cy = 185, 175
    face_base(draw, cx, cy, 120, 100)
    eye_closed(draw, cx - 45, cy - 20)
    eye_closed(draw, cx + 45, cy - 20)
    # sleeping mouth (small line)
    draw.arc([cx - 25, cy + 20, cx + 25, cy + 45], 10, 170, fill=OUTLINE, width=5)
    # zzz
    for i, (zx, zy, sz) in enumerate([(cx + 90, cy - 60, 20), (cx + 108, cy - 85, 26), (cx + 128, cy - 115, 32)]):
        draw.text((zx, zy), "z", fill=BLUE, font=ImageFont.load_default(size=sz))
    return img


def sticker_surprised() -> Image.Image:
    img, draw = new_canvas()
    cx, cy = 185, 160
    face_base(draw, cx, cy, 120, 110)
    eye(draw, cx - 45, cy - 20, 20)
    eye(draw, cx + 45, cy - 20, 20)
    # highlight dots
    for ex in (cx - 45, cx + 45):
        draw.ellipse([ex - 8, cy - 35, ex - 1, cy - 28], fill=WHITE)
    mouth_open(draw, cx, cy + 30, 35, 35)
    return img


def sticker_thumbsup() -> Image.Image:
    img, draw = new_canvas()
    # face slightly left
    cx, cy = 150, 160
    face_base(draw, cx, cy, 105, 100)
    eye_closed(draw, cx - 38, cy - 15)
    eye_closed(draw, cx + 38, cy - 15)
    mouth_smile(draw, cx, cy + 15, 55, 28)
    cheek(draw, cx - 65, cy + 5)
    cheek(draw, cx + 65, cy + 5)
    # thumb
    thumb_cx = 290
    draw.rectangle([thumb_cx - 18, cy - 20, thumb_cx + 18, cy + 60], fill=YELLOW, outline=OUTLINE, width=5)
    draw.ellipse([thumb_cx - 22, cy - 60, thumb_cx + 22, cy - 10], fill=YELLOW, outline=OUTLINE, width=5)
    draw.rectangle([thumb_cx - 28, cy + 20, thumb_cx + 28, cy + 70], fill=YELLOW, outline=OUTLINE, width=5)
    return img


def sticker_wave() -> Image.Image:
    img, draw = new_canvas()
    cx, cy = 160, 170
    face_base(draw, cx, cy, 100, 95)
    eye_closed(draw, cx - 35, cy - 15)
    eye_closed(draw, cx + 35, cy - 15)
    mouth_smile(draw, cx, cy + 10, 55, 30)
    cheek(draw, cx - 65, cy)
    cheek(draw, cx + 65, cy)
    # waving hand (arc-based)
    hx, hy = 285, 120
    draw.ellipse([hx - 38, hy - 55, hx + 38, hy + 55], fill=YELLOW, outline=OUTLINE, width=5)
    # fingers as small ovals
    for angle_deg, (fx, fy) in zip(
        [-60, -30, 0, 30, 60],
        [(hx - 30, hy - 65), (hx - 10, hy - 75), (hx + 12, hy - 72), (hx + 30, hy - 62), (hx + 42, hy - 45)],
    ):
        draw.ellipse([fx - 10, fy - 18, fx + 10, fy + 5], fill=YELLOW, outline=OUTLINE, width=4)
    return img


STICKERS: list[tuple[str, callable]] = [
    ("01_happy", sticker_happy),
    ("02_sad", sticker_sad),
    ("03_love", sticker_love),
    ("04_angry", sticker_angry),
    ("05_sleeping", sticker_sleeping),
    ("06_surprised", sticker_surprised),
    ("07_thumbsup", sticker_thumbsup),
    ("08_wave", sticker_wave),
]


def make_tab_icon(first_sticker: Image.Image) -> Image.Image:
    """Scale the first sticker down to the tab icon size."""
    return first_sticker.resize((TAB_W, TAB_H), Image.LANCZOS)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    first_img = None

    for name, fn in STICKERS:
        img = fn()
        path = os.path.join(OUT_DIR, f"{name}.png")
        img.save(path, "PNG")
        print(f"  saved {path}")
        if first_img is None:
            first_img = img

    tab = make_tab_icon(first_img)
    tab_path = os.path.join(OUT_DIR, "tab_icon.png")
    tab.save(tab_path, "PNG")
    print(f"  saved {tab_path}")

    print(f"\nDone! {len(STICKERS)} stickers + 1 tab icon -> ./{OUT_DIR}/")


if __name__ == "__main__":
    main()
