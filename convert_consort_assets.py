"""Convert Umbral Consort source art to CK3 DDS assets."""
from PIL import Image, ImageEnhance
import os

SESSION = r"X:\Users\USER\.grok\sessions\C%3A%5CUsers%5CUSER\019f2379-fcad-7c81-b0d9-c08690713797\images"
MOD = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lasombra_court"))

SOURCES = {
    "decision": ("47.jpg", (1100, 440), "gfx/interface/illustrations/decisions/lasombra_court_umbral_consort_decision.dds"),
    "event": ("46.jpg", (1592, 848), "gfx/interface/illustrations/event_scenes/lasombra_court_umbral_consort.dds"),
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


def enhance(img):
    rgb = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.08)
    rgb = ImageEnhance.Color(rgb).enhance(1.1)
    return rgb.convert("RGBA")


def main():
    for key, (src, size, rel) in SOURCES.items():
        src_path = os.path.join(SESSION, src)
        out_path = os.path.join(MOD, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        img = Image.open(src_path).convert("RGBA")
        img = crop_cover(img, *size)
        out = enhance(img)
        out.save(out_path)
        print(f"wrote {key}: {out_path} {size}")


if __name__ == "__main__":
    main()