"""
LINE sticker generator — chibi salaryman character.

Based on a real person's features:
  - Dark hair (medium length, slightly tousled)
  - Dark navy suit + white dress shirt
  - Expressive face, signature open-hand shrug pose

LINE sticker specs:
  Main image: 370 x 320 px, PNG, ≤ 1 MB
  Tab icon:    96 x  74 px, PNG
"""

import os
from PIL import Image, ImageDraw

STICKER_W, STICKER_H = 370, 320
TAB_W, TAB_H = 96, 74
OUT_DIR = "stickers"

# ── palette ────────────────────────────────────────────────────────────────────
TRANSPARENT   = (0,   0,   0,   0)
SKIN          = (240, 195, 155, 255)
SKIN_SHADOW   = (210, 160, 120, 255)
HAIR          = (45,  30,  20,  255)
HAIR_HI       = (80,  55,  35,  255)
SUIT          = (50,  55,  85,  255)
SUIT_SHADOW   = (30,  35,  60,  255)
SHIRT         = (245, 245, 250, 255)
SHIRT_SHADOW  = (200, 205, 215, 255)
OUTLINE       = (30,  25,  20,  255)
WHITE         = (255, 255, 255, 255)
BLACK         = (20,  20,  20,  255)
RED           = (220, 60,  60,  255)
PINK          = (255, 160, 180, 255)
BLUE          = (80,  130, 220, 255)
YELLOW        = (255, 220, 50,  255)
SWEAT         = (150, 200, 240, 255)

OL = OUTLINE   # shorthand
OW = 4         # default outline width


# ── low-level helpers ──────────────────────────────────────────────────────────

def new_canvas():
    img = Image.new("RGBA", (STICKER_W, STICKER_H), TRANSPARENT)
    return img, ImageDraw.Draw(img)


def ell(draw, cx, cy, rx, ry, fill, outline=OL, width=OW):
    box = [cx - rx, cy - ry, cx + rx, cy + ry]
    draw.ellipse(box, fill=outline)
    draw.ellipse([cx - rx + width, cy - ry + width,
                  cx + rx - width, cy + ry - width], fill=fill)


def rect(draw, x0, y0, x1, y1, fill, outline=OL, width=OW):
    draw.rectangle([x0 - width, y0 - width, x1 + width, y1 + width], fill=outline)
    draw.rectangle([x0, y0, x1, y1], fill=fill)


# ── face components ────────────────────────────────────────────────────────────

def draw_face(draw, cx, cy, rx=72, ry=68):
    """Round chibi face."""
    ell(draw, cx, cy, rx, ry, SKIN)
    # subtle jaw shadow
    draw.ellipse([cx - rx + 10, cy + ry // 2, cx + rx - 10, cy + ry + 6],
                 fill=SKIN_SHADOW)


def draw_hair(draw, cx, cy, rx=72, ry=68):
    """Dark hair covering the top of the head."""
    # main hair cap
    draw.ellipse([cx - rx - 2, cy - ry - 2, cx + rx + 2, cy + 8],
                 fill=OL)
    draw.ellipse([cx - rx + 4, cy - ry + 4, cx + rx - 4, cy + 10],
                 fill=HAIR)
    # tousled tufts on top
    tufts = [(-28, -ry - 14, 18, 22), (0, -ry - 18, 18, 22),
             (26, -ry - 12, 16, 20)]
    for dx, dy, tw, th in tufts:
        draw.ellipse([cx + dx - tw // 2 - 2, cy + dy - th // 2 - 2,
                      cx + dx + tw // 2 + 2, cy + dy + th // 2 + 2],
                     fill=OL)
        draw.ellipse([cx + dx - tw // 2, cy + dy - th // 2,
                      cx + dx + tw // 2, cy + dy + th // 2],
                     fill=HAIR)
    # hair highlight
    draw.ellipse([cx - 20, cy - ry + 6, cx + 8, cy - ry + 18],
                 fill=HAIR_HI)


def draw_eyes_normal(draw, cx, cy):
    ex_l, ex_r, ey = cx - 28, cx + 28, cy - 8
    for ex in (ex_l, ex_r):
        ell(draw, ex, ey, 13, 13, BLACK, WHITE, 3)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(60, 40, 20, 255))
        draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=BLACK)
        draw.ellipse([ex + 2, ey - 6, ex + 7, ey - 1], fill=WHITE)


def draw_eyes_closed_happy(draw, cx, cy):
    ey = cy - 8
    for ex in (cx - 28, cx + 28):
        draw.arc([ex - 13, ey - 6, ex + 13, ey + 6],
                 200, 340, fill=OL, width=5)


def draw_eyes_wide(draw, cx, cy):
    ey = cy - 8
    for ex in (cx - 28, cx + 28):
        ell(draw, ex, ey, 15, 16, BLACK, WHITE, 3)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=BLACK)
        draw.ellipse([ex + 2, ey - 7, ex + 8, ey - 1], fill=WHITE)


def draw_eyes_teary(draw, cx, cy):
    ey = cy - 8
    for ex in (cx - 28, cx + 28):
        ell(draw, ex, ey, 13, 15, BLACK, WHITE, 3)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=BLACK)
        draw.ellipse([ex + 2, ey - 6, ex + 7, ey - 1], fill=WHITE)
        # lower lid shimmer
        draw.arc([ex - 13, ey + 2, ex + 13, ey + 18], 0, 180,
                 fill=BLUE, width=3)


def draw_eyes_angry(draw, cx, cy):
    ey = cy - 8
    for ex in (cx - 28, cx + 28):
        ell(draw, ex, ey, 13, 12, BLACK, WHITE, 3)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=BLACK)
    # angry brows
    draw.line([cx - 44, cy - 28, cx - 18, cy - 20], fill=OL, width=5)
    draw.line([cx + 18, cy - 20, cx + 44, cy - 28], fill=OL, width=5)


def draw_eyebrows(draw, cx, cy):
    draw.line([cx - 44, cy - 26, cx - 16, cy - 22], fill=OL, width=4)
    draw.line([cx + 16, cy - 22, cx + 44, cy - 26], fill=OL, width=4)


def draw_mouth_smile(draw, cx, cy, w=40, h=22):
    draw.arc([cx - w, cy + 8, cx + w, cy + 8 + h * 2],
             10, 170, fill=OL, width=5)


def draw_mouth_open_laugh(draw, cx, cy):
    draw.ellipse([cx - 30, cy + 5, cx + 30, cy + 32], fill=OL)
    draw.ellipse([cx - 24, cy + 9, cx + 24, cy + 30], fill=RED)
    draw.ellipse([cx - 16, cy + 20, cx + 16, cy + 30], fill=(200, 80, 80, 255))


def draw_mouth_sad(draw, cx, cy):
    draw.arc([cx - 35, cy + 18, cx + 35, cy + 50],
             195, 345, fill=OL, width=5)


def draw_mouth_flat(draw, cx, cy):
    draw.line([cx - 25, cy + 18, cx + 25, cy + 18], fill=OL, width=5)


def draw_mouth_shout(draw, cx, cy):
    draw.ellipse([cx - 22, cy + 5, cx + 22, cy + 35], fill=OL)
    draw.ellipse([cx - 17, cy + 9, cx + 17, cy + 33], fill=RED)


def draw_sweat(draw, cx, cy):
    """Single sweat drop on forehead."""
    sx, sy = cx + 58, cy - 30
    draw.polygon([(sx, sy - 16), (sx - 8, sy + 8), (sx + 8, sy + 8)],
                 fill=SWEAT)
    draw.ellipse([sx - 8, sy + 4, sx + 8, sy + 18], fill=SWEAT)


def draw_cheeks(draw, cx, cy):
    for dx in (-55, 55):
        draw.ellipse([cx + dx - 18, cy + 5, cx + dx + 18, cy + 20],
                     fill=(*PINK[:3], 150))


# ── body components ────────────────────────────────────────────────────────────

def draw_body_suit(draw, cx, by):
    """Simple chibi suit torso."""
    # jacket
    draw.polygon([
        (cx - 55, by),
        (cx + 55, by),
        (cx + 70, by + 90),
        (cx - 70, by + 90),
    ], fill=SUIT_SHADOW)
    draw.polygon([
        (cx - 50, by),
        (cx + 50, by),
        (cx + 62, by + 85),
        (cx - 62, by + 85),
    ], fill=SUIT)
    # shirt / tie gap
    draw.polygon([
        (cx - 14, by),
        (cx + 14, by),
        (cx + 10, by + 70),
        (cx - 10, by + 70),
    ], fill=SHIRT)
    # lapels
    draw.polygon([(cx, by + 10), (cx - 14, by), (cx - 38, by + 30)],
                 fill=SUIT_SHADOW)
    draw.polygon([(cx, by + 10), (cx + 14, by), (cx + 38, by + 30)],
                 fill=SUIT_SHADOW)
    # collar
    draw.polygon([(cx - 14, by), (cx, by + 12), (cx - 5, by)],
                 fill=SHIRT_SHADOW)
    draw.polygon([(cx + 14, by), (cx, by + 12), (cx + 5, by)],
                 fill=SHIRT_SHADOW)


def draw_arms_down(draw, cx, by):
    """Arms hanging at sides."""
    for side in (-1, 1):
        x0 = cx + side * 58
        draw.ellipse([x0 - 16, by + 5, x0 + 16, by + 75],
                     fill=SUIT, outline=OL, width=3)
        # hand
        ell(draw, x0, by + 80, 14, 12, SKIN)


def draw_arms_shrug(draw, cx, by):
    """Signature open-hands shrug pose."""
    for side in (-1, 1):
        # upper arm going outward and slightly up
        ax = cx + side * 75
        ay = by + 20
        draw.polygon([
            (cx + side * 55, by + 5),
            (cx + side * 55, by + 35),
            (ax + side * 10, ay + 45),
            (ax + side * 20, ay + 30),
        ], fill=SUIT, outline=OL)
        # forearm rotated outward / palm up
        fx = ax + side * 22
        fy = ay + 48
        draw.polygon([
            (ax + side * 5,  ay + 30),
            (ax + side * 20, ay + 30),
            (fx + side * 12, fy + 10),
            (fx - side * 2,  fy + 10),
        ], fill=SUIT, outline=OL)
        # open palm
        palm_cx = fx + side * 6
        palm_cy = fy + 20
        ell(draw, palm_cx, palm_cy, 18, 14, SKIN)
        # fingers spread
        for i, (fdx, fdy) in enumerate([
            (-10, -14), (-3, -17), (5, -16), (13, -12), (18, -4)
        ]):
            ell(draw, palm_cx + fdx * side, palm_cy + fdy,
                5, 9, SKIN, OL, 2)


def draw_arms_thumbsup(draw, cx, by):
    """Left arm down, right arm raised with thumb up."""
    # left arm down
    x0 = cx - 62
    draw.ellipse([x0 - 14, by + 5, x0 + 14, by + 72],
                 fill=SUIT, outline=OL, width=3)
    ell(draw, x0, by + 77, 13, 11, SKIN)
    # right arm raised
    draw.polygon([
        (cx + 55, by + 5),
        (cx + 72, by + 5),
        (cx + 88, by - 30),
        (cx + 70, by - 35),
    ], fill=SUIT, outline=OL)
    # fist
    ell(draw, cx + 80, by - 45, 16, 14, SKIN)
    # thumb up
    draw.polygon([
        (cx + 74, by - 45),
        (cx + 70, by - 72),
        (cx + 82, by - 72),
        (cx + 86, by - 45),
    ], fill=SKIN, outline=OL)
    ell(draw, cx + 78, by - 74, 10, 9, SKIN)


def draw_arms_wave(draw, cx, by):
    """One arm raised and waving."""
    # left arm down
    x0 = cx - 62
    draw.ellipse([x0 - 14, by + 5, x0 + 14, by + 72],
                 fill=SUIT, outline=OL, width=3)
    ell(draw, x0, by + 77, 13, 11, SKIN)
    # right arm up + open hand
    draw.polygon([
        (cx + 55, by + 5),
        (cx + 70, by + 5),
        (cx + 100, by - 40),
        (cx + 85, by - 48),
    ], fill=SUIT, outline=OL)
    ell(draw, cx + 94, by - 56, 17, 15, SKIN)
    for i, (fdx, fdy) in enumerate([(-10, -16), (-3, -19), (6, -18),
                                     (14, -12), (18, -3)]):
        ell(draw, cx + 94 + fdx, by - 56 + fdy, 5, 9, SKIN, OL, 2)


def draw_arms_facepalm(draw, cx, by):
    """Both hands raised to face."""
    for side in (-1, 1):
        ax = cx + side * 28
        draw.polygon([
            (cx + side * 52, by + 10),
            (cx + side * 62, by + 10),
            (ax + side * 10, by - 20),
            (ax - side * 2,  by - 20),
        ], fill=SUIT, outline=OL)
        ell(draw, ax + side * 4, by - 28, 17, 14, SKIN)


def draw_arms_crossed(draw, cx, by):
    """Arms folded across chest."""
    draw.polygon([
        (cx - 62, by + 10), (cx - 48, by + 10),
        (cx + 30, by + 45), (cx + 22, by + 55),
    ], fill=SUIT_SHADOW, outline=OL)
    draw.polygon([
        (cx + 62, by + 10), (cx + 48, by + 10),
        (cx - 30, by + 45), (cx - 22, by + 55),
    ], fill=SUIT, outline=OL)


def draw_arms_point(draw, cx, by):
    """Right arm pointing forward / at viewer."""
    x0 = cx - 62
    draw.ellipse([x0 - 14, by + 5, x0 + 14, by + 72],
                 fill=SUIT, outline=OL, width=3)
    ell(draw, x0, by + 77, 13, 11, SKIN)
    # pointing arm
    draw.polygon([
        (cx + 55, by + 15), (cx + 68, by + 8),
        (cx + 95, by + 30), (cx + 82, by + 40),
    ], fill=SUIT, outline=OL)
    ell(draw, cx + 98, by + 35, 14, 12, SKIN)
    # index finger extended
    draw.polygon([
        (cx + 102, by + 26),
        (cx + 120, by + 14),
        (cx + 125, by + 22),
        (cx + 108, by + 34),
    ], fill=SKIN, outline=OL)
    ell(draw, cx + 122, by + 16, 7, 7, SKIN)


# ── full character builder ─────────────────────────────────────────────────────

def draw_character(draw, cx, cy,
                   eyes_fn=None, mouth_fn=None, arms_fn=None,
                   face_fn=None,
                   extra_fn=None):
    face_rx, face_ry = 72, 68
    body_top = cy + face_ry - 5

    if arms_fn:
        arms_fn(draw, cx, body_top)

    draw_body_suit(draw, cx, body_top)
    draw_face(draw, cx, cy, face_rx, face_ry)
    draw_hair(draw, cx, cy, face_rx, face_ry)

    if face_fn:
        face_fn(draw, cx, cy)
    else:
        draw_eyebrows(draw, cx, cy)
        (eyes_fn or draw_eyes_normal)(draw, cx, cy)
        (mouth_fn or draw_mouth_smile)(draw, cx, cy)

    if extra_fn:
        extra_fn(draw, cx, cy)


# ── 8 stickers ─────────────────────────────────────────────────────────────────

def sticker_shrug() -> Image.Image:
    """Signature shrug / 'dunno' pose."""
    img, draw = new_canvas()
    cx, cy = 185, 148
    draw_character(draw, cx, cy,
                   eyes_fn=draw_eyes_normal,
                   mouth_fn=draw_mouth_flat,
                   arms_fn=draw_arms_shrug)
    # question marks
    for qx, qy in ((60, 50), (315, 50)):
        draw.text((qx, qy), "?", fill=(*YELLOW[:3], 220))
    return img


def sticker_laugh() -> Image.Image:
    """Big happy laugh."""
    img, draw = new_canvas()
    cx, cy = 185, 148
    draw_character(draw, cx, cy,
                   eyes_fn=draw_eyes_closed_happy,
                   mouth_fn=draw_mouth_open_laugh,
                   arms_fn=draw_arms_down)
    draw_cheeks(draw, cx, cy)
    return img


def sticker_thumbsup() -> Image.Image:
    """Thumbs-up / good."""
    img, draw = new_canvas()
    cx, cy = 180, 148
    draw_character(draw, cx, cy,
                   eyes_fn=draw_eyes_closed_happy,
                   mouth_fn=draw_mouth_smile,
                   arms_fn=draw_arms_thumbsup)
    draw_cheeks(draw, cx, cy)
    return img


def sticker_wave() -> Image.Image:
    """Waving hello/goodbye."""
    img, draw = new_canvas()
    cx, cy = 175, 148
    draw_character(draw, cx, cy,
                   eyes_fn=draw_eyes_closed_happy,
                   mouth_fn=draw_mouth_smile,
                   arms_fn=draw_arms_wave)
    draw_cheeks(draw, cx, cy)
    return img


def sticker_surprised() -> Image.Image:
    """Wide-eyed surprise."""
    img, draw = new_canvas()
    cx, cy = 185, 148
    draw_character(draw, cx, cy,
                   eyes_fn=draw_eyes_wide,
                   mouth_fn=draw_mouth_shout,
                   arms_fn=draw_arms_down)
    draw_sweat(draw, cx, cy)
    return img


def sticker_troubled() -> Image.Image:
    """Troubled / facepalm."""
    img, draw = new_canvas()
    cx, cy = 185, 148
    draw_character(draw, cx, cy,
                   eyes_fn=draw_eyes_teary,
                   mouth_fn=draw_mouth_sad,
                   arms_fn=draw_arms_facepalm)
    draw_sweat(draw, cx, cy)
    return img


def sticker_serious() -> Image.Image:
    """Serious / arms crossed."""
    img, draw = new_canvas()
    cx, cy = 185, 148
    draw_character(draw, cx, cy,
                   eyes_fn=draw_eyes_normal,
                   mouth_fn=draw_mouth_flat,
                   arms_fn=draw_arms_crossed)
    return img


def sticker_point() -> Image.Image:
    """Pointing — 'you!' or 'go!'"""
    img, draw = new_canvas()
    cx, cy = 178, 148
    draw_character(draw, cx, cy,
                   eyes_fn=draw_eyes_wide,
                   mouth_fn=draw_mouth_shout,
                   arms_fn=draw_arms_point)
    return img


STICKERS: list[tuple[str, callable]] = [
    ("01_shrug",     sticker_shrug),
    ("02_laugh",     sticker_laugh),
    ("03_thumbsup",  sticker_thumbsup),
    ("04_wave",      sticker_wave),
    ("05_surprised", sticker_surprised),
    ("06_troubled",  sticker_troubled),
    ("07_serious",   sticker_serious),
    ("08_point",     sticker_point),
]


def make_tab_icon(first_sticker: Image.Image) -> Image.Image:
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
