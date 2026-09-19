"""Convert generated trait art to 120x120 DDS for CK3."""
from PIL import Image, ImageEnhance
import os

SESSION_IMAGES = r"X:\Users\USER\.grok\sessions\C%3A%5CUsers%5CUSER\019f2379-fcad-7c81-b0d9-c08690713797\images"
OUT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "gfx", "interface", "icons", "traits")
)
TARGET = (120, 120)

MAPPING = {
    "lasombra_court_penumbra_born": "37.jpg",
    "lasombra_court_mirrorless": "38.jpg",
    "lasombra_court_friend_of_night": "39.jpg",
    "lasombra_court_shadow_consort": "40.jpg",
    "lasombra_court_blood_arbiter": "41.jpg",
    "lasombra_court_living_shadow": "42.jpg",
    "lasombra_court_ash_liturgist": "43.jpg",
}


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


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, src in MAPPING.items():
        src_path = os.path.join(SESSION_IMAGES, src)
        img = Image.open(src_path).convert("RGBA")
        img = crop_cover(img, *TARGET)
        rgb = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.08)
        rgb = ImageEnhance.Color(rgb).enhance(1.1)
        out = rgb.convert("RGBA")
        out.save(os.path.join(OUT_DIR, f"{name}.dds"))
        print("wrote", name)


if __name__ == "__main__":
    main()