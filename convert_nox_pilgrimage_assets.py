"""Build Pilgrimage of Nox Tenebrarum activity icons + header background."""
import importlib.util
import os
import shutil
import tempfile

from PIL import Image, ImageEnhance

from dds_compress import (
    compress_dds_dxt1,
    finalize_activity_header_dds,
    finalize_activity_icon_dds,
    finalize_activity_title_icon_dds,
)

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(TOOLS, "..", "lasombra_court"))

# Shadow-lit ritual hall — fits multi-city void pilgrimage better than orgy art
SOURCE = os.path.join(
    TOOLS, "activity_scene_sources", "lasombra_court_pursuit_shadow_chant.jpg"
)
SOURCE_COPY = os.path.join(TOOLS, "source_nox_tenebrarum_pilgrimage.jpg")

ACTIVITY_KEY = "activity_lasombra_court_nox_tenebrarum_pilgrimage"
ACTIVITY_ICON_SIZE = (80, 80)
ACTIVITY_TITLE_ICON_SIZE = (164, 164)

OUTPUTS = {
    "event": (
        (1592, 848),
        os.path.join(
            MOD,
            "gfx",
            "interface",
            "illustrations",
            "event_scenes",
            "lasombra_court_nox_tenebrarum_pilgrimage.dds",
        ),
        compress_dds_dxt1,
    ),
    "header": (
        (1100, 440),
        os.path.join(
            MOD,
            "gfx",
            "interface",
            "illustrations",
            "activity_header_backgrounds",
            f"{ACTIVITY_KEY}.dds",
        ),
        finalize_activity_header_dds,
    ),
    "icon": (
        ACTIVITY_ICON_SIZE,
        os.path.join(
            MOD,
            "gfx",
            "interface",
            "icons",
            "activities",
            f"{ACTIVITY_KEY}.dds",
        ),
        finalize_activity_icon_dds,
    ),
    "title_icon": (
        ACTIVITY_TITLE_ICON_SIZE,
        os.path.join(
            MOD,
            "gfx",
            "interface",
            "icons",
            "activities",
            f"{ACTIVITY_KEY}_header.dds",
        ),
        finalize_activity_title_icon_dds,
    ),
}


def load_council_converter():
    path = os.path.join(TOOLS, "convert_umbral_council_assets.py")
    spec = importlib.util.spec_from_file_location("convert_umbral_council_assets", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    # Slightly cooler / darker for Abyss pilgrimage read in Activities tab
    rgb = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.08)
    rgb = ImageEnhance.Color(rgb).enhance(0.92)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.94)
    return rgb.convert("RGBA")


def make_round_activity_icon(converter, size):
    task_icon = converter.make_task_icon(SOURCE_COPY)
    return task_icon.resize(size, Image.LANCZOS)


def main():
    if not os.path.exists(SOURCE):
        raise FileNotFoundError(SOURCE)

    shutil.copy2(SOURCE, SOURCE_COPY)
    img = Image.open(SOURCE).convert("RGBA")
    converter = load_council_converter()

    for key, (size, out_path, finalize) in OUTPUTS.items():
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        if key in ("icon", "title_icon"):
            out = make_round_activity_icon(converter, size)
        else:
            out = enhance(crop_cover(img, *size))
        with tempfile.NamedTemporaryFile(suffix=".dds", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            out.save(tmp_path)
            finalize(tmp_path)
            shutil.move(tmp_path, out_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        print(f"wrote {key}: {out_path} {size}")


if __name__ == "__main__":
    main()
