"""Generate Ethos Umbral banner (1200x260) for CK3 culture pillar UI."""
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os

SESSION = r"X:\Users\USER\.grok\sessions\C%3A%5CUsers%5CUSER\019f2379-fcad-7c81-b0d9-c08690713797\images"
MOD = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lasombra_court"))
BANNER_SIZE = (1200, 260)
OUT = os.path.join(MOD, "gfx", "interface", "icons", "culture_pillars", "ethos_umbral.dds")

MIRROR = os.path.join(MOD, "gfx", "interface", "icons", "faith", "via_tenebrarum_mirror_custom.dds")
CHALICE = os.path.join(MOD, "gfx", "interface", "icons", "faith", "via_tenebrarum_chalice_custom.dds")
SCENE_SRC = os.path.join(SESSION, "46.jpg")


def crop_cover(img, tw, th):
    w, h = img.size
    target_ratio = tw / th
    src_ratio = w / h
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((tw, th), Image.LANCZOS)


def edge_vignette(size, side_width=0.12, floor=0.55):
    w, h = size
    mask = Image.new("L", size, 255)
    draw = ImageDraw.Draw(mask)
    fade = int(w * side_width)
    for x in range(fade):
        alpha = int(255 * (floor + (1 - floor) * (x / fade)))
        draw.line((x, 0, x, h), fill=alpha)
        draw.line((w - 1 - x, 0, w - 1 - x, h), fill=alpha)
    return mask


def paste_centered(base, overlay, x, y, opacity=1.0):
    if overlay.mode != "RGBA":
        overlay = overlay.convert("RGBA")
    if opacity < 1.0:
        alpha = overlay.split()[3].point(lambda a: int(a * opacity))
        overlay = overlay.copy()
        overlay.putalpha(alpha)
    base.paste(overlay, (x, y), overlay)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    scene = Image.open(SCENE_SRC).convert("RGBA")
    scene = crop_cover(scene, *BANNER_SIZE)
    scene = ImageEnhance.Contrast(scene.convert("RGB")).enhance(1.1)
    scene = ImageEnhance.Color(scene).enhance(1.05)
    base = scene.convert("RGBA")

    tint = Image.new("RGBA", BANNER_SIZE, (20, 12, 40, 45))
    base = Image.alpha_composite(base, tint)

    mirror = Image.open(MIRROR).convert("RGBA")
    mirror = crop_cover(mirror, 180, 180)
    paste_centered(base, mirror, 28, 40, opacity=0.92)

    chalice = Image.open(CHALICE).convert("RGBA")
    chalice = crop_cover(chalice, 130, 130)
    paste_centered(base, chalice, 1040, 65, opacity=0.88)

    accent = Image.new("RGBA", BANNER_SIZE, (0, 0, 0, 0))
    ad = ImageDraw.Draw(accent)
    ad.rectangle((0, BANNER_SIZE[1] - 3, BANNER_SIZE[0], BANNER_SIZE[1]), fill=(140, 105, 50, 160))
    base = Image.alpha_composite(base, accent)

    dark = Image.new("RGBA", BANNER_SIZE, (8, 5, 18, 255))
    base = Image.composite(base, dark, edge_vignette(BANNER_SIZE))

    out = base.filter(ImageFilter.UnsharpMask(radius=1.0, percent=115, threshold=3))
    out.save(OUT)
    print(f"wrote {OUT} {BANNER_SIZE}")


if __name__ == "__main__":
    main()