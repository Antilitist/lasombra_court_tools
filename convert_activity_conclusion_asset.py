"""Convert orgyend.jpg into the Court of Shadows activity conclusion scene."""
from PIL import Image, ImageEnhance
import os
import shutil

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(TOOLS, "..", "lasombra_court"))

SOURCE = r"X:\Users\USER\Pictures\CK3Mod\orgyend.jpg"
SOURCE_COPY = os.path.join(TOOLS, "source_activity_conclusion_orgyend.jpg")
OUTPUT = os.path.join(
    MOD,
    "gfx",
    "interface",
    "illustrations",
    "event_scenes",
    "lasombra_court_activity_conclusion.dds",
)
EVENT_SCENE_SIZE = (1592, 848)


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


def enhance(img):
    rgb = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.06)
    rgb = ImageEnhance.Color(rgb).enhance(1.08)
    return rgb.convert("RGBA")


def main():
    if not os.path.exists(SOURCE):
        raise FileNotFoundError(SOURCE)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    shutil.copy2(SOURCE, SOURCE_COPY)

    img = Image.open(SOURCE).convert("RGBA")
    out = enhance(crop_cover(img, *EVENT_SCENE_SIZE))
    out.save(OUTPUT)
    print("wrote", OUTPUT, EVENT_SCENE_SIZE)


if __name__ == "__main__":
    main()