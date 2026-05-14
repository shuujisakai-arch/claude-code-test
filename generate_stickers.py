"""
LINE sticker generator — Toriyama Akira art style.

Style hallmarks:
  - Thick clean outlines (7-8 px)
  - Large expressive eyes (white sclera, iris, pupil, highlight)
  - Tiny button nose (two small dots)
  - Hair drawn as bold defined polygon chunks
  - Flat vibrant colours, minimal shading
  - Dynamic chibi proportions

LINE specs: main 370x320 px PNG, tab icon 96x74 px
"""

import os
from PIL import Image, ImageDraw

STICKER_W, STICKER_H = 370, 320
TAB_W, TAB_H = 96, 74
OUT_DIR = "stickers"

# ── palette ────────────────────────────────────────────────────────────────────
T   = (0,0,0,0)            # transparent
OL  = (20,15,10,255)       # outline (near-black, warm)
OW  = 7                    # outline width

SKIN     = (252, 210, 165, 255)
SKIN_D   = (225, 175, 130, 255)   # shadow/chin
HAIR     = (40,  28,  16,  255)
HAIR_HI  = (90,  65,  40,  255)
SUIT     = (55,  60,  95,  255)
SUIT_D   = (35,  38,  68,  255)
SHIRT    = (248, 248, 252, 255)
EYE_W    = (255, 255, 255, 255)
IRIS     = (60,  35,  15,  255)
PUPIL    = (15,  10,   5,  255)
HILITE   = (255, 255, 255, 255)
RED      = (230,  55,  50, 255)
PINK     = (255, 155, 175, 255)
BLUE     = (90,  145, 230, 255)
YELLOW   = (255, 225,  40, 255)
SWEAT    = (140, 200, 245, 255)
BLUSH    = (245, 140, 155, 180)
ANGER    = (220,  50,  50, 255)
TEAR     = (120, 185, 240, 200)


def new_canvas():
    img = Image.new("RGBA", (STICKER_W, STICKER_H), T)
    return img, ImageDraw.Draw(img)


# ── primitives ─────────────────────────────────────────────────────────────────

def outlined_ellipse(draw, cx, cy, rx, ry, fill, ow=OW):
    draw.ellipse([cx-rx-ow, cy-ry-ow, cx+rx+ow, cy+ry+ow], fill=OL)
    draw.ellipse([cx-rx,    cy-ry,    cx+rx,    cy+ry   ], fill=fill)

def outlined_polygon(draw, pts, fill, ow=OW):
    import math
    # draw outline by stroking the polygon path
    draw.polygon(pts, fill=OL)
    # shrink each point toward centroid by ow pixels
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    inner = []
    for x, y in pts:
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy) or 1
        inner.append((x - dx/d*ow, y - dy/d*ow))
    draw.polygon(inner, fill=fill)

def outlined_rect(draw, x0, y0, x1, y1, fill, ow=OW):
    draw.rectangle([x0-ow, y0-ow, x1+ow, y1+ow], fill=OL)
    draw.rectangle([x0,    y0,    x1,    y1   ], fill=fill)


# ── face ───────────────────────────────────────────────────────────────────────

def draw_face(draw, cx, cy, rx=80, ry=74):
    outlined_ellipse(draw, cx, cy+4, rx, ry, SKIN)
    # chin highlight
    draw.ellipse([cx-rx+18, cy+ry-18, cx+rx-18, cy+ry+10], fill=SKIN_D)

def draw_hair_toriyama(draw, cx, cy, rx=80):
    """Bold defined hair chunks — Toriyama style."""
    top = cy - 74
    # main hair mass (solid cap)
    draw.ellipse([cx-rx-4, top-6, cx+rx+4, cy-10], fill=OL)
    draw.ellipse([cx-rx+4, top+2, cx+rx-4, cy-12], fill=HAIR)
    # side hair — left
    draw.polygon([
        (cx-rx+5, cy-30),
        (cx-rx-8, cy+10),
        (cx-rx+12, cy+5),
        (cx-rx+20, cy-20),
    ], fill=OL)
    draw.polygon([
        (cx-rx+9,  cy-26),
        (cx-rx-2,  cy+6),
        (cx-rx+14, cy+2),
        (cx-rx+22, cy-18),
    ], fill=HAIR)
    # side hair — right
    draw.polygon([
        (cx+rx-5,  cy-30),
        (cx+rx+8,  cy+10),
        (cx+rx-12, cy+5),
        (cx+rx-20, cy-20),
    ], fill=OL)
    draw.polygon([
        (cx+rx-9,  cy-26),
        (cx+rx+2,  cy+6),
        (cx+rx-14, cy+2),
        (cx+rx-22, cy-18),
    ], fill=HAIR)
    # forelock / tousled bang in front
    draw.polygon([
        (cx-30, top+8),
        (cx-18, top-10),
        (cx-4,  top+5),
        (cx+10, top-8),
        (cx+24, top+6),
        (cx+14, top+22),
        (cx-20, top+24),
    ], fill=OL)
    draw.polygon([
        (cx-26, top+12),
        (cx-18, top-4),
        (cx-4,  top+9),
        (cx+10, top-2),
        (cx+22, top+10),
        (cx+12, top+21),
        (cx-18, top+22),
    ], fill=HAIR)
    # hair highlight streak
    draw.polygon([
        (cx-22, top+6), (cx-14, top+3),
        (cx+6,  top+8), (cx-2,  top+13),
    ], fill=HAIR_HI)


# ── eyes ───────────────────────────────────────────────────────────────────────

def draw_eye_toriyama(draw, cx, cy, rx=16, ry=14):
    """Single Toriyama eye: sclera → iris → pupil → highlight."""
    outlined_ellipse(draw, cx, cy, rx, ry, EYE_W, ow=4)
    # iris
    draw.ellipse([cx-9, cy-8, cx+9, cy+8], fill=IRIS)
    # pupil
    draw.ellipse([cx-5, cy-4, cx+5, cy+6], fill=PUPIL)
    # upper shadow on sclera
    draw.ellipse([cx-rx+2, cy-ry+1, cx+rx-2, cy], fill=(220,220,225,180))
    # highlight
    draw.ellipse([cx+3, cy-7, cx+9, cy-1], fill=HILITE)

def draw_eyes_normal(draw, cx, cy):
    draw_eye_toriyama(draw, cx-30, cy-4)
    draw_eye_toriyama(draw, cx+30, cy-4)

def draw_eyes_happy(draw, cx, cy):
    """Squinting happy arcs."""
    for ex in (cx-30, cx+30):
        draw.arc([ex-16, cy-12, ex+16, cy+4], 200, 340, fill=OL, width=6)

def draw_eyes_wide(draw, cx, cy):
    """Huge shocked eyes."""
    for ex in (cx-30, cx+30):
        outlined_ellipse(draw, ex, cy-4, 18, 17, EYE_W, ow=4)
        draw.ellipse([ex-10, cy-13, ex+10, cy+5], fill=IRIS)
        draw.ellipse([ex-6,  cy-9,  ex+6,  cy+3], fill=PUPIL)
        draw.ellipse([ex+4,  cy-12, ex+10, cy-6], fill=HILITE)

def draw_eyes_angry(draw, cx, cy):
    for ex, slope in ((cx-30, 1), (cx+30, -1)):
        outlined_ellipse(draw, ex, cy-2, 16, 13, EYE_W, ow=4)
        draw.ellipse([ex-8, cy-9, ex+8, cy+5], fill=IRIS)
        draw.ellipse([ex-4, cy-6, ex+4, cy+3], fill=PUPIL)
        draw.ellipse([ex+3, cy-8, ex+8, cy-3], fill=HILITE)
    # heavy angled brows
    draw.line([cx-50, cy-28+8, cx-14, cy-22+3], fill=OL, width=8)
    draw.line([cx+14, cy-22+3, cx+50, cy-28+8], fill=OL, width=8)

def draw_eyes_teary(draw, cx, cy):
    draw_eyes_normal(draw, cx, cy)
    for ex in (cx-30, cx+30):
        draw.ellipse([ex-14, cy+10, ex+14, cy+22], fill=TEAR)
        draw.ellipse([ex-6,  cy+20, ex+6,  cy+38], fill=(*BLUE[:3], 180))

def draw_eyes_closed_smile(draw, cx, cy):
    for ex in (cx-30, cx+30):
        draw.arc([ex-16, cy-8, ex+16, cy+8], 195, 345, fill=OL, width=6)

def draw_eyebrows(draw, cx, cy):
    for ex, slope_y in ((cx-30, 2), (cx+30, -2)):
        draw.line([ex-18, cy-26+slope_y, ex+18, cy-22-slope_y//2],
                  fill=OL, width=6)


# ── nose & mouth ───────────────────────────────────────────────────────────────

def draw_nose(draw, cx, cy):
    """Two small dots — classic Toriyama."""
    for dx in (-7, 7):
        draw.ellipse([cx+dx-4, cy+10, cx+dx+4, cy+18], fill=SKIN_D)

def draw_mouth_grin(draw, cx, cy):
    draw.arc([cx-32, cy+16, cx+32, cy+48], 10, 170, fill=OL, width=6)

def draw_mouth_laugh(draw, cx, cy):
    """Open mouth with teeth — Toriyama big laugh."""
    draw.ellipse([cx-28, cy+14, cx+28, cy+42], fill=OL)
    draw.ellipse([cx-22, cy+18, cx+22, cy+40], fill=RED)
    # upper teeth row
    draw.rectangle([cx-20, cy+18, cx+20, cy+27], fill=EYE_W)
    draw.line([cx, cy+18, cx, cy+27], fill=(200,200,205,255), width=2)

def draw_mouth_shout(draw, cx, cy):
    draw.ellipse([cx-20, cy+14, cx+20, cy+42], fill=OL)
    draw.ellipse([cx-15, cy+18, cx+15, cy+40], fill=RED)

def draw_mouth_flat(draw, cx, cy):
    draw.line([cx-22, cy+22, cx+22, cy+22], fill=OL, width=6)

def draw_mouth_sad(draw, cx, cy):
    draw.arc([cx-28, cy+28, cx+28, cy+52], 195, 345, fill=OL, width=6)

def draw_mouth_smirk(draw, cx, cy):
    draw.arc([cx-10, cy+16, cx+34, cy+40], 10, 130, fill=OL, width=6)

def draw_mouth_nervous(draw, cx, cy):
    """Wavy nervous line."""
    pts = []
    import math
    for i in range(20):
        t = i / 19
        x = int(cx - 28 + 56 * t)
        y = int(cy + 22 + math.sin(t * math.pi * 3) * 5)
        pts.append((x, y))
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=OL, width=5)

def draw_blush(draw, cx, cy):
    for dx in (-56, 56):
        draw.ellipse([cx+dx-20, cy+8, cx+dx+20, cy+24], fill=BLUSH)


# ── body ───────────────────────────────────────────────────────────────────────

def draw_suit_body(draw, cx, by):
    # jacket silhouette
    outlined_polygon(draw, [
        (cx-60, by), (cx+60, by),
        (cx+75, by+100), (cx-75, by+100),
    ], SUIT)
    # shirt strip
    outlined_polygon(draw, [
        (cx-16, by), (cx+16, by),
        (cx+12, by+80), (cx-12, by+80),
    ], SHIRT)
    # left lapel
    outlined_polygon(draw, [
        (cx-16, by), (cx, by+14), (cx-42, by+38), (cx-58, by+12),
    ], SUIT_D)
    # right lapel
    outlined_polygon(draw, [
        (cx+16, by), (cx, by+14), (cx+42, by+38), (cx+58, by+12),
    ], SUIT_D)

def arm_sleeve(draw, pts, fill=SUIT):
    """Draw a sleeve (polygon) with outline."""
    outlined_polygon(draw, pts, fill)

def hand(draw, cx, cy, r=13):
    outlined_ellipse(draw, cx, cy, r, r-2, SKIN)

def finger(draw, cx, cy, angle_deg, length=18, r=5):
    import math
    a = math.radians(angle_deg)
    ex = cx + math.cos(a) * length
    ey = cy + math.sin(a) * length
    draw.line([cx, cy, ex, ey], fill=OL, width=r*2+2)
    draw.line([cx, cy, ex, ey], fill=SKIN, width=r*2-2)
    outlined_ellipse(draw, int(ex), int(ey), r, r, SKIN, ow=3)


# ── arm poses ─────────────────────────────────────────────────────────────────

def arms_shrug(draw, cx, by):
    for side in (-1, 1):
        # upper arm angled out
        ax = cx + side * 85
        arm_sleeve(draw, [
            (cx + side*58, by+8),
            (cx + side*65, by+38),
            (ax + side*14, by+55),
            (ax + side*4,  by+28),
        ])
        # forearm / palm-up
        arm_sleeve(draw, [
            (ax + side*2,  by+28),
            (ax + side*16, by+55),
            (ax + side*28, by+85),
            (ax + side*14, by+80),
        ])
        # open palm
        palm_cx = ax + side * 22
        palm_cy = by + 92
        outlined_ellipse(draw, palm_cx, palm_cy, 16, 12, SKIN)
        # spread fingers
        for ang, (fdx, fdy) in zip(
            [-90, -65, -45, -20, 10],
            [(-2,-20),(-12,-16),(-18,-8),(-16,4),(-8,14)]
        ):
            finger(draw, palm_cx + fdx*side, palm_cy + fdy, ang*side, 14, 4)

def arms_down(draw, cx, by):
    for side in (-1, 1):
        arm_sleeve(draw, [
            (cx + side*58, by+6),
            (cx + side*72, by+6),
            (cx + side*74, by+80),
            (cx + side*60, by+80),
        ])
        hand(draw, cx + side*67, by+90)

def arms_thumbsup(draw, cx, by):
    # left arm down
    arm_sleeve(draw, [
        (cx-58, by+6), (cx-72, by+6),
        (cx-74, by+80), (cx-60, by+80),
    ])
    hand(draw, cx-67, by+90)
    # right arm raised
    arm_sleeve(draw, [
        (cx+58, by+6),  (cx+72, by+10),
        (cx+95, by-40), (cx+80, by-46),
    ])
    # fist
    outlined_ellipse(draw, cx+90, by-56, 15, 13, SKIN)
    # thumb
    outlined_polygon(draw, [
        (cx+82, by-50), (cx+78, by-82),
        (cx+90, by-84), (cx+95, by-52),
    ], SKIN)
    outlined_ellipse(draw, cx+85, by-84, 10, 9, SKIN)

def arms_wave(draw, cx, by):
    arm_sleeve(draw, [
        (cx-58, by+6), (cx-72, by+6),
        (cx-74, by+80), (cx-60, by+80),
    ])
    hand(draw, cx-67, by+90)
    # raised arm
    arm_sleeve(draw, [
        (cx+58, by+8), (cx+72, by+4),
        (cx+105, by-46), (cx+90, by-52),
    ])
    outlined_ellipse(draw, cx+99, by-60, 15, 14, SKIN)
    for ang, length in [(-100,16),(-75,18),(-50,18),(-25,16),(0,13)]:
        finger(draw, cx+99, by-60, ang, length, 4)

def arms_crossed(draw, cx, by):
    # right over left
    arm_sleeve(draw, [
        (cx-60, by+14), (cx-46, by+10),
        (cx+38, by+46), (cx+28, by+58),
    ])
    arm_sleeve(draw, [
        (cx+60, by+14), (cx+46, by+10),
        (cx-38, by+46), (cx-28, by+58),
    ], SUIT_D)

def arms_point(draw, cx, by):
    arm_sleeve(draw, [
        (cx-58, by+6), (cx-72, by+6),
        (cx-74, by+80), (cx-60, by+80),
    ])
    hand(draw, cx-67, by+90)
    arm_sleeve(draw, [
        (cx+58, by+16), (cx+72, by+8),
        (cx+108, by+36), (cx+94, by+48),
    ])
    outlined_ellipse(draw, cx+110, by+44, 14, 12, SKIN)
    finger(draw, cx+118, by+40, -25, 22, 5)

def arms_facepalm(draw, cx, by):
    for side in (-1, 1):
        arm_sleeve(draw, [
            (cx + side*56, by+12),
            (cx + side*68, by+8),
            (cx + side*36, by-24),
            (cx + side*22, by-20),
        ])
        outlined_ellipse(draw, cx + side*28, by-30, 16, 13, SKIN)


# ── extra fx ───────────────────────────────────────────────────────────────────

def sweat_drop(draw, cx, cy, ox=62, oy=-38):
    sx, sy = cx+ox, cy+oy
    draw.polygon([(sx, sy-18),(sx-9, sy+6),(sx+9, sy+6)], fill=SWEAT)
    draw.ellipse([sx-9, sy+2, sx+9, sy+20], fill=SWEAT)
    # outline
    draw.arc([sx-9, sy-18, sx+9, sy+22], 0, 360, fill=(*BLUE[:3],180), width=2)

def anger_mark(draw, cx, cy, ox=72, oy=-55):
    ax, ay = cx+ox, cy+oy
    c = ANGER
    w = 4
    draw.line([ax, ay, ax+12, ay-8], fill=c, width=w)
    draw.line([ax+12, ay-8, ax+20, ay+4], fill=c, width=w)
    draw.line([ax+20, ay+4, ax+10, ay+10], fill=c, width=w)

def question_marks(draw, cx, cy):
    for qx, qy, sz in ((68, 45, 32), (302, 45, 32)):
        draw.text((qx, qy), "?", fill=(*YELLOW[:3], 230))

def sparkles(draw, cx, cy):
    import math
    for i, (ox, oy, r) in enumerate([(-80,-55,8),(85,-60,6),(-95,-30,5)]):
        sx, sy = cx+ox, cy+oy
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            draw.line([sx, sy,
                       int(sx+math.cos(a)*r*2),
                       int(sy+math.sin(a)*r*2)],
                      fill=YELLOW, width=3)
        draw.ellipse([sx-r,sy-r,sx+r,sy+r], fill=YELLOW)


# ── full character ─────────────────────────────────────────────────────────────

def character(draw, cx, cy,
              eyes_fn=draw_eyes_normal,
              mouth_fn=draw_mouth_grin,
              arms_fn=arms_down,
              extra_fn=None,
              brows=True):
    face_ry = 74
    body_top = cy + face_ry - 6

    arms_fn(draw, cx, body_top)
    draw_suit_body(draw, cx, body_top)
    draw_face(draw, cx, cy)
    draw_hair_toriyama(draw, cx, cy)
    if brows:
        draw_eyebrows(draw, cx, cy)
    eyes_fn(draw, cx, cy)
    draw_nose(draw, cx, cy)
    mouth_fn(draw, cx, cy)
    if extra_fn:
        extra_fn(draw, cx, cy)


# ── 8 stickers ─────────────────────────────────────────────────────────────────

def s_shrug() -> Image.Image:
    img, draw = new_canvas()
    character(draw, 185, 145,
              eyes_fn=draw_eyes_normal,
              mouth_fn=draw_mouth_flat,
              arms_fn=arms_shrug,
              extra_fn=question_marks)
    return img

def s_laugh() -> Image.Image:
    img, draw = new_canvas()
    character(draw, 185, 145,
              eyes_fn=draw_eyes_happy,
              mouth_fn=draw_mouth_laugh,
              arms_fn=arms_down,
              extra_fn=lambda d,cx,cy: (draw_blush(d,cx,cy), sparkles(d,cx,cy)))
    return img

def s_thumbsup() -> Image.Image:
    img, draw = new_canvas()
    character(draw, 178, 145,
              eyes_fn=draw_eyes_closed_smile,
              mouth_fn=draw_mouth_grin,
              arms_fn=arms_thumbsup,
              extra_fn=lambda d,cx,cy: draw_blush(d,cx,cy))
    return img

def s_wave() -> Image.Image:
    img, draw = new_canvas()
    character(draw, 172, 145,
              eyes_fn=draw_eyes_closed_smile,
              mouth_fn=draw_mouth_grin,
              arms_fn=arms_wave,
              extra_fn=lambda d,cx,cy: draw_blush(d,cx,cy))
    return img

def s_surprised() -> Image.Image:
    img, draw = new_canvas()
    character(draw, 185, 145,
              eyes_fn=draw_eyes_wide,
              mouth_fn=draw_mouth_shout,
              arms_fn=arms_down,
              extra_fn=lambda d,cx,cy: sweat_drop(d,cx,cy))
    return img

def s_troubled() -> Image.Image:
    img, draw = new_canvas()
    character(draw, 185, 145,
              eyes_fn=draw_eyes_teary,
              mouth_fn=draw_mouth_nervous,
              arms_fn=arms_facepalm,
              extra_fn=lambda d,cx,cy: sweat_drop(d,cx,cy,62,-38))
    return img

def s_angry() -> Image.Image:
    img, draw = new_canvas()
    character(draw, 185, 145,
              eyes_fn=draw_eyes_angry,
              mouth_fn=draw_mouth_shout,
              arms_fn=arms_crossed,
              brows=False,
              extra_fn=lambda d,cx,cy: anger_mark(d,cx,cy))
    return img

def s_point() -> Image.Image:
    img, draw = new_canvas()
    character(draw, 178, 145,
              eyes_fn=draw_eyes_wide,
              mouth_fn=draw_mouth_shout,
              arms_fn=arms_point)
    return img


STICKERS = [
    ("01_shrug",     s_shrug),
    ("02_laugh",     s_laugh),
    ("03_thumbsup",  s_thumbsup),
    ("04_wave",      s_wave),
    ("05_surprised", s_surprised),
    ("06_troubled",  s_troubled),
    ("07_angry",     s_angry),
    ("08_point",     s_point),
]


def make_tab_icon(first: Image.Image) -> Image.Image:
    return first.resize((TAB_W, TAB_H), Image.LANCZOS)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    first = None
    for name, fn in STICKERS:
        img = fn()
        path = os.path.join(OUT_DIR, f"{name}.png")
        img.save(path, "PNG")
        print(f"  saved {path}")
        if first is None:
            first = img
    tab_path = os.path.join(OUT_DIR, "tab_icon.png")
    make_tab_icon(first).save(tab_path, "PNG")
    print(f"  saved {tab_path}")
    print(f"\nDone! {len(STICKERS)} stickers + tab icon → ./{OUT_DIR}/")


if __name__ == "__main__":
    main()
