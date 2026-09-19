"""Batch-build Court of Shadows activity event scene DDS files (1592x848).

Drop source art into tools/activity_scene_sources/<basename>.jpg (or .png).
Missing sources are copied from procession/veiled pursuit fallbacks so the mod
loads until custom art is ready.

Usage:
    python tools/convert_activity_scene_backgrounds.py
    python tools/convert_activity_scene_backgrounds.py --seed-only
"""
from PIL import Image, ImageEnhance
import argparse
import os
import shutil
import tempfile

from dds_compress import compress_dds_dxt1

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(TOOLS, "..", "lasombra_court"))
SOURCES = os.path.join(TOOLS, "activity_scene_sources")
OUT_DIR = os.path.join(MOD, "gfx", "interface", "illustrations", "event_scenes")
EVENT_SIZE = (1592, 848)

FALLBACK_PROCESSION = os.path.join(OUT_DIR, "lasombra_court_umbral_orgy.dds")
FALLBACK_PURSUIT = os.path.join(OUT_DIR, "lasombra_court_veiled_pursuit.dds")

PROCESSION_SCENES = (
    "lasombra_court_procession_nave_open",
    "lasombra_court_procession_vigil_tone",
    "lasombra_court_procession_confession_rail",
    "lasombra_court_procession_blood_wine",
    "lasombra_court_procession_pulse_confession",
    "lasombra_court_procession_pulse_indulgence",
    "lasombra_court_procession_pulse_sanctify",
    "lasombra_court_procession_pulse_ash",
    "lasombra_court_procession_pulse_blood",
    "lasombra_court_procession_pulse_seductive",
    "lasombra_court_procession_pulse_carnal",
    "lasombra_court_procession_pulse_benediction",
    "lasombra_court_procession_pulse_wine",
)

PURSUIT_SCENES = (
    "lasombra_court_veiled_pursuit",
    "lasombra_court_pursuit_veil_descend",
    "lasombra_court_pursuit_night_tone",
    "lasombra_court_pursuit_corridor_hunt",
    "lasombra_court_pursuit_pre_dawn",
    "lasombra_court_pursuit_conclusion",
    "lasombra_court_pursuit_initiation_font",
    "lasombra_court_pursuit_seeker_claims",
    "lasombra_court_pursuit_veil_lifted",
    "lasombra_court_pursuit_foreign_oath",
    "lasombra_court_pursuit_rival_mask",
    "lasombra_court_pursuit_oath_long_night",
    "lasombra_court_pursuit_veil_refused",
    "lasombra_court_pursuit_blood_wine_hunt",
    "lasombra_court_pursuit_salon_votary",
    "lasombra_court_pursuit_shadow_chant",
)


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


def find_source(basename):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = os.path.join(SOURCES, basename + ext)
        if os.path.exists(path):
            return path
    return None


def write_from_image(src_path, out_path):
    img = enhance(crop_cover(Image.open(src_path).convert("RGBA"), *EVENT_SIZE))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".dds", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        img.save(tmp_path)
        compress_dds_dxt1(tmp_path)
        shutil.move(tmp_path, out_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    print(f"converted {os.path.basename(src_path)} -> {out_path}")


def seed_copy(fallback, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if not os.path.exists(out_path):
        shutil.copy2(fallback, out_path)
        print(f"seeded {out_path}")


def process_scene(basename, fallback, seed_only=False):
    out_path = os.path.join(OUT_DIR, f"{basename}.dds")
    src = find_source(basename)
    if src and not seed_only:
        write_from_image(src, out_path)
    else:
        seed_copy(fallback, out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-only", action="store_true", help="copy fallbacks only")
    args = parser.parse_args()

    if not os.path.exists(FALLBACK_PROCESSION):
        raise FileNotFoundError(FALLBACK_PROCESSION)
    if not os.path.exists(FALLBACK_PURSUIT):
        raise FileNotFoundError(FALLBACK_PURSUIT)

    os.makedirs(SOURCES, exist_ok=True)

    for name in PROCESSION_SCENES:
        process_scene(name, FALLBACK_PROCESSION, seed_only=args.seed_only)
    for name in PURSUIT_SCENES:
        process_scene(name, FALLBACK_PURSUIT, seed_only=args.seed_only)


if __name__ == "__main__":
    main()