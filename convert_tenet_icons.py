"""Convert generated tenet PNG/JPG art to 260x400 DDS for CK3."""
from PIL import Image, ImageEnhance
import os

SESSION_IMAGES = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", ".grok", "sessions",
                 "C%3A%5CUsers%5CUSER", "019f2379-fcad-7c81-b0d9-c08690713797", "images")
)
# Fallback absolute path
SESSION_IMAGES = r"X:\Users\USER\.grok\sessions\C%3A%5CUsers%5CUSER\019f2379-fcad-7c81-b0d9-c08690713797\images"

OUT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "gfx", "interface", "icons", "faith_doctrines")
)
TARGET = (260, 400)

MAPPING = {
    "lasombra_tenet_court_of_blood": "23.jpg",
    "lasombra_tenet_obtenebration": "24.jpg",
    "lasombra_tenet_amici_noctis": "21.jpg",
    "lasombra_tenet_blood_absolution": "22.jpg",
    "lasombra_tenet_sanguine_bonds": "27.jpg",
    "lasombra_tenet_iron_nocturne": "26.jpg",
    "lasombra_tenet_shadow_harem": "28.jpg",
    "lasombra_tenet_trophy_skulls": "25.jpg",
    "lasombra_tenet_chalice_eclipse": "29.jpg",
    "lasombra_tenet_noble_shadows": "32.jpg",
    "lasombra_tenet_veiled_hunger": "31.jpg",
    "lasombra_tenet_ash_liturgy": "30.jpg",
    "lasombra_tenet_veiled_faith": "36.jpg",
    "lasombra_tenet_abyssal_lore": "34.jpg",
    "lasombra_tenet_saturnalia_tenebris": "35.jpg",
    "lasombra_tenet_smoke_of_abyss": "33.jpg",
    "lasombra_tenet_blood_flock": "70.jpg",
}


def crop_cover(img, target_w, target_h):
    tw, th = target_w, target_h
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


def process(src_path, dst_path):
    img = Image.open(src_path).convert("RGBA")
    img = crop_cover(img, *TARGET)
    # Slight contrast/saturation boost to match Umbral culture icons
    rgb = img.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    rgb = ImageEnhance.Color(rgb).enhance(1.12)
    out = rgb.convert("RGBA")
    out.save(dst_path)
    print("wrote", dst_path, out.size)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, src in MAPPING.items():
        src_path = os.path.join(SESSION_IMAGES, src)
        if not os.path.exists(src_path):
            raise FileNotFoundError(src_path)
        process(src_path, os.path.join(OUT_DIR, f"{name}.dds"))


if __name__ == "__main__":
    main()