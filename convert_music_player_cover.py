"""Build the Court of Shadows music player category cover (648x376)."""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

MOD = (Path(__file__).resolve().parents[1] / "lasombra_court")
SOURCE = MOD / "thumbnail.png"
OUTPUT = (
    MOD
    / "gfx"
    / "interface"
    / "illustrations"
    / "music_player"
    / "lasombra_court_soundtrack_list.dds"
)
PREVIEW = MOD / "tools" / "preview_lasombra_court_soundtrack_list.png"
SIZE = (648, 376)


def crop_cover(img: Image.Image, tw: int, th: int) -> Image.Image:
    w, h = img.size
    target_ratio = tw / th
    src_ratio = w / h
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = max(0, int((h - new_h) * 0.18))
        img = img.crop((0, top, w, top + new_h))
    return img.resize((tw, th), Image.LANCZOS)


def vignette(img: Image.Image) -> Image.Image:
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((-w * 0.12, -h * 0.18, w * 1.12, h * 1.18), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=18))
    dark = Image.new("RGBA", (w, h), (8, 4, 12, 255))
    return Image.composite(img, dark, mask)


def enhance(img: Image.Image) -> Image.Image:
    rgb = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.08)
    rgb = ImageEnhance.Color(rgb).enhance(1.05)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.94)
    return rgb.convert("RGBA")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base = Image.open(SOURCE).convert("RGBA")
    out = enhance(vignette(crop_cover(base, *SIZE)))
    out.save(OUTPUT)
    out.save(PREVIEW)
    print(f"wrote {OUTPUT} {SIZE}")
    print(f"wrote {PREVIEW}")


if __name__ == "__main__":
    main()