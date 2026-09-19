#!/usr/bin/env python3
"""Install Salon of Night custom art into CoS lifestyle GFX.

Sources (square JPGs):
  D:\\My CK3 Mods\\Art\\Salon of Night\\

Outputs (mod paths, CK3 sizes):
  icons/lifestyles/salon_of_night_lifestyle.dds              480x160 (3x160 frames)
  icons/lifestyle_tree_backgrounds/{salon_whispers,ash_liturgy,
                                    iron_nocturne,sanguine_court}.dds
  icons/focuses/{*_focus}.dds                                  140x140

Does NOT overwrite illustrations/lifestyles_background/salon_of_night_lifestyle.dds
(the tall 608×1552 panel stays the prior custom art).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

ART = r"D:\My CK3 Mods\Art\Salon of Night"
MOD = os.path.normpath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lasombra_court")
)
GFX = os.path.join(MOD, "gfx", "interface")
TEXCONV = os.environ.get(
    "TEXCONV",
    r"X:\Users\USER\AppData\Local\Microsoft\WinGet\Links\texconv.exe",
)

# (source filename, dest relative to gfx/interface, size, kind)
JOBS = [
    (
        "Salon of Whispers.jpg",
        os.path.join("icons", "lifestyle_tree_backgrounds", "salon_whispers.dds"),
        (500, 812),
        "tree",
    ),
    (
        "Ash Liturgy.jpg",
        os.path.join("icons", "lifestyle_tree_backgrounds", "ash_liturgy.dds"),
        (348, 812),
        "tree",
    ),
    (
        "Iron Nocturne.jpg",
        os.path.join("icons", "lifestyle_tree_backgrounds", "iron_nocturne.dds"),
        (348, 812),
        "tree",
    ),
    (
        "Sanguine Court.jpg",
        os.path.join("icons", "lifestyle_tree_backgrounds", "sanguine_court.dds"),
        (500, 812),
        "tree",
    ),
    (
        "Salon of Whispers.jpg",
        os.path.join("icons", "focuses", "salon_whispers_focus.dds"),
        (140, 140),
        "focus",
    ),
    (
        "Ash Liturgy.jpg",
        os.path.join("icons", "focuses", "ash_liturgy_focus.dds"),
        (140, 140),
        "focus",
    ),
    (
        "Iron Nocturne.jpg",
        os.path.join("icons", "focuses", "iron_nocturne_focus.dds"),
        (140, 140),
        "focus",
    ),
    (
        "Sanguine Court.jpg",
        os.path.join("icons", "focuses", "sanguine_court_focus.dds"),
        (140, 140),
        "focus",
    ),
]


def crop_cover(img: Image.Image, tw: int, th: int, bias: float = 0.5) -> Image.Image:
    w, h = img.size
    target_ratio = tw / th
    src_ratio = w / h
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = int((w - new_w) * bias)
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = int((h - new_h) * bias)
        img = img.crop((0, top, w, top + new_h))
    return img.resize((tw, th), Image.LANCZOS)


def grade(img: Image.Image, *, brightness: float = 1.05, contrast: float = 1.08, color: float = 1.06) -> Image.Image:
    rgb = img.convert("RGB")
    rgb = ImageEnhance.Brightness(rgb).enhance(brightness)
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    rgb = ImageEnhance.Color(rgb).enhance(color)
    return rgb.convert("RGBA")


def key_white_to_alpha(img: Image.Image, threshold: int = 232, softness: int = 18) -> Image.Image:
    """Knock out paper-white backgrounds so only the medallion remains."""
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            mn = min(r, g, b)
            mx = max(r, g, b)
            if mn >= threshold and (mx - mn) <= 28:
                px[x, y] = (r, g, b, 0)
            elif mn >= threshold - softness and (mx - mn) <= 40:
                t = (mn - (threshold - softness)) / float(softness)
                px[x, y] = (r, g, b, int(a * (1.0 - t)))
    return img


def circular_mask(size: int, margin: int = 1) -> Image.Image:
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse((margin, margin, size - 1 - margin, size - 1 - margin), fill=255)
    return m.filter(ImageFilter.GaussianBlur(radius=0.8))


def apply_circle_alpha(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    mask = circular_mask(img.size[0])
    r, g, b, a = img.split()
    a = ImageChops.multiply(a, mask)
    return Image.merge("RGBA", (r, g, b, a))


def make_focus_icon(src: Image.Image, size: int = 140) -> Image.Image:
    src = key_white_to_alpha(src)
    side = min(src.size)
    left = (src.width - side) // 2
    top = (src.height - side) // 2
    square = src.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)
    square = grade(square, brightness=1.08, contrast=1.1, color=1.08)
    square = key_white_to_alpha(square)
    return apply_circle_alpha(square)


def make_lifestyle_tab_icon(src: Image.Image) -> Image.Image:
    """480x160 strip: three 160x160 frames. Outside the circles is fully transparent."""
    src = key_white_to_alpha(src)

    def frame(*, brightness: float, contrast: float, color: float, desaturate: float = 0.0) -> Image.Image:
        f = crop_cover(src, 160, 160, bias=0.5)
        rgb = f.convert("RGB")
        rgb = ImageEnhance.Brightness(rgb).enhance(brightness)
        rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
        if desaturate > 0.5:
            rgb = ImageEnhance.Color(rgb).enhance(0.15)
        else:
            rgb = ImageEnhance.Color(rgb).enhance(color)
        out = key_white_to_alpha(rgb.convert("RGBA"))
        return apply_circle_alpha(out)

    available = frame(brightness=1.02, contrast=1.06, color=1.05)
    selected = frame(brightness=1.12, contrast=1.12, color=1.10)
    muted = frame(brightness=0.78, contrast=0.95, color=0.4, desaturate=0.85)

    strip = Image.new("RGBA", (480, 160), (0, 0, 0, 0))
    strip.paste(available, (0, 0), available)
    strip.paste(selected, (160, 0), selected)
    strip.paste(muted, (320, 0), muted)
    return strip


def write_dds_texconv(img: Image.Image, dest: str) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "src.png")
        img.save(png, "PNG")
        if os.path.isfile(TEXCONV):
            subprocess.run(
                [TEXCONV, "-f", "BC3_UNORM", "-y", "-o", tmp, png],
                check=True,
                capture_output=True,
            )
            produced = None
            for name in os.listdir(tmp):
                if name.lower().endswith(".dds"):
                    produced = os.path.join(tmp, name)
                    break
            if not produced:
                raise FileNotFoundError("texconv produced no DDS")
            shutil.copy2(produced, dest)
        else:
            img.save(dest)
    print(f"wrote {dest} ({img.size[0]}x{img.size[1]})")


def main() -> int:
    salon = os.path.join(ART, "Salon of Night.jpg")
    if not os.path.isfile(salon):
        print(f"Missing source art: {salon}", file=sys.stderr)
        return 1

    src_salon = Image.open(salon).convert("RGBA")
    tab = make_lifestyle_tab_icon(src_salon)
    write_dds_texconv(tab, os.path.join(GFX, "icons", "lifestyles", "salon_of_night_lifestyle.dds"))

    for src_name, rel, size, kind in JOBS:
        src_path = os.path.join(ART, src_name)
        if not os.path.isfile(src_path):
            print(f"SKIP missing {src_path}", file=sys.stderr)
            continue
        src = Image.open(src_path).convert("RGBA")
        tw, th = size
        if kind == "focus":
            out = make_focus_icon(src, tw)
        else:
            out = grade(crop_cover(src, tw, th, bias=0.45), brightness=1.04, contrast=1.08, color=1.06)
        write_dds_texconv(out, os.path.join(GFX, rel))

    print("Salon of Night art install complete (tall panel left untouched).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
