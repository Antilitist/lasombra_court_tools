"""Convert Umbral Legion MaA source art to CK3 DDS assets.

Sources: tools/army/<maa_key>.jpg
Outputs:
  gfx/interface/illustrations/men_at_arms_big/<maa_key>.dds   (680x400)
  gfx/interface/illustrations/men_at_arms_small/<maa_key>.dds (160x160)
  gfx/interface/icons/regimenttypes/<maa_key>.dds               (120x120)

Preview PNGs are written to tools/army/previews/ for quick review.
"""
from PIL import Image, ImageEnhance
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(TOOLS, "..", "lasombra_court"))
SRC_DIR = os.path.join(TOOLS, "army")
PREVIEW_DIR = os.path.join(SRC_DIR, "previews")

OUT_BIG = os.path.join(MOD, "gfx", "interface", "illustrations", "men_at_arms_big")
OUT_SMALL = os.path.join(MOD, "gfx", "interface", "illustrations", "men_at_arms_small")
OUT_ICON = os.path.join(MOD, "gfx", "interface", "icons", "regimenttypes")

# anchor_x / anchor_y bias the cover crop (0 = top/left, 1 = bottom/right).
UNITS = {
    "lasombra_court_ash_legionnaires": {
        "big": (680, 400, 0.50, 0.40),
        "small": (160, 160, 0.50, 0.55),
        "icon": (120, 120, 0.48, 0.60),
    },
    "lasombra_court_chapel_lancers": {
        "big": (680, 400, 0.22, 0.50),
        "small": (160, 160, 0.28, 0.52),
        "icon": (120, 120, 0.30, 0.48),
    },
    "lasombra_court_confessors_ram": {
        "big": (680, 400, 0.30, 0.48),
        "small": (160, 160, 0.35, 0.50),
        "icon": (120, 120, 0.32, 0.46),
    },
}


def crop_cover(img, tw, th, anchor_x=0.5, anchor_y=0.5):
    w, h = img.size
    target_ratio = tw / th
    src_ratio = w / h
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = int((w - new_w) * anchor_x)
        left = max(0, min(left, w - new_w))
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = int((h - new_h) * anchor_y)
        top = max(0, min(top, h - new_h))
        img = img.crop((0, top, w, top + new_h))
    return img.resize((tw, th), Image.LANCZOS)


def enhance(img, *, contrast=1.08, color=1.10, sharpness=1.05):
    rgb = ImageEnhance.Contrast(img.convert("RGB")).enhance(contrast)
    rgb = ImageEnhance.Color(rgb).enhance(color)
    rgb = ImageEnhance.Sharpness(rgb).enhance(sharpness)
    return rgb.convert("RGBA")


def save_asset(img, dds_path, preview_path):
    os.makedirs(os.path.dirname(dds_path), exist_ok=True)
    os.makedirs(os.path.dirname(preview_path), exist_ok=True)
    img.save(dds_path)
    img.convert("RGB").save(preview_path)


def main():
    for key, crops in UNITS.items():
        src_path = os.path.join(SRC_DIR, f"{key}.jpg")
        if not os.path.isfile(src_path):
            raise FileNotFoundError(src_path)

        base = Image.open(src_path).convert("RGBA")

        for label, (tw, th, ax, ay) in crops.items():
            cropped = crop_cover(base, tw, th, ax, ay)
            if label == "icon":
                out = enhance(cropped, contrast=1.12, color=1.12, sharpness=1.15)
            elif label == "small":
                out = enhance(cropped, contrast=1.10, color=1.10, sharpness=1.10)
            else:
                out = enhance(cropped)

            if label == "big":
                out_dir = OUT_BIG
            elif label == "small":
                out_dir = OUT_SMALL
            else:
                out_dir = OUT_ICON

            dds_path = os.path.join(out_dir, f"{key}.dds")
            preview_path = os.path.join(PREVIEW_DIR, f"{key}_{label}.png")
            save_asset(out, dds_path, preview_path)
            print(f"wrote {label:5} {tw}x{th} -> {dds_path}")

    print(f"previews -> {PREVIEW_DIR}")


if __name__ == "__main__":
    main()