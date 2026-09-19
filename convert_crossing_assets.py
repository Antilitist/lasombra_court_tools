"""Build Umbral Crossing ceremony event scene DDS files (1592x848)."""
from PIL import Image, ImageEnhance
import os
import shutil
import tempfile

from dds_compress import compress_dds_dxt1

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(TOOLS, "..", "lasombra_court"))
SOURCES = os.path.join(TOOLS, "crossing_scene_sources")
OUT_DIR = os.path.join(MOD, "gfx", "interface", "illustrations", "event_scenes")
EVENT_SIZE = (1592, 848)

SCENES = {
    "lasombra_court_crossing_terms": ("crossing_terms.jpg", "lasombra_court_procession_pulse_seductive.dds", {"contrast": 1.05, "color": 1.1, "tint": (40, 15, 50)}),
    "lasombra_court_crossing_heaven": ("crossing_heaven.jpg", "lasombra_court_procession_pulse_carnal.dds", {"contrast": 1.08, "color": 1.15, "tint": (55, 10, 35)}),
    "lasombra_court_crossing_vigil": ("crossing_vigil.jpg", "lasombra_court_procession_pulse_ash.dds", {"contrast": 1.1, "color": 0.95, "tint": (25, 20, 30)}),
    "lasombra_court_crossing_bite": ("crossing_bite.jpg", "lasombra_court_procession_pulse_blood.dds", {"contrast": 1.12, "color": 1.08, "tint": (45, 5, 15)}),
    "lasombra_court_crossing_awakening": ("crossing_awakening.jpg", "lasombra_court_umbral_consort.dds", {"contrast": 1.06, "color": 1.05, "tint": (30, 10, 45)}),
    "lasombra_court_crossing_court": ("crossing_court.jpg", "lasombra_court_umbral_orgy.dds", {"contrast": 1.08, "color": 1.1, "tint": (35, 12, 40)}),
    "lasombra_court_crossing_afterglow": ("crossing_afterglow.jpg", "lasombra_court_pursuit_pre_dawn.dds", {"contrast": 1.04, "color": 1.12, "tint": (50, 25, 55)}),
    "lasombra_court_crossing_covenant": ("crossing_covenant.jpg", "lasombra_court_umbral_consort.dds", {"contrast": 1.07, "color": 1.14, "tint": (60, 12, 40)}),
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


def apply_tint(img, tint_rgb, strength=0.18):
    tint = Image.new("RGB", img.size, tint_rgb)
    base = img.convert("RGB")
    return Image.blend(base, tint, strength).convert("RGBA")


def enhance(img, opts):
    rgb = ImageEnhance.Contrast(img.convert("RGB")).enhance(opts.get("contrast", 1.06))
    rgb = ImageEnhance.Color(rgb).enhance(opts.get("color", 1.05))
    return apply_tint(rgb, opts.get("tint", (30, 10, 35)), opts.get("tint_strength", 0.16))


def load_source(source_name, fallback_name):
    src_path = os.path.join(SOURCES, source_name)
    if os.path.isfile(src_path):
        return Image.open(src_path).convert("RGBA")
    fallback_path = os.path.join(OUT_DIR, fallback_name)
    if os.path.isfile(fallback_path):
        return Image.open(fallback_path).convert("RGBA")
    raise FileNotFoundError(f"no source for {source_name} or fallback {fallback_name}")


def write_scene(name, img):
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{name}.dds")
    with tempfile.NamedTemporaryFile(suffix=".dds", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        img.save(tmp_path)
        compress_dds_dxt1(tmp_path)
        shutil.move(tmp_path, out_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    print("wrote", out_path)


def ff_source_name(source_name):
    base, ext = os.path.splitext(source_name)
    return f"{base}_ff{ext}"


def build_scene(scene_name, source_name, fallback, opts):
    img = load_source(source_name, fallback)
    img = crop_cover(img, *EVENT_SIZE)
    img = enhance(img, opts)
    write_scene(scene_name, img)


def main():
    os.makedirs(SOURCES, exist_ok=True)
    for scene_name, (source_name, fallback, opts) in SCENES.items():
        build_scene(scene_name, source_name, fallback, opts)
        ff_source = ff_source_name(source_name)
        if os.path.isfile(os.path.join(SOURCES, ff_source)):
            build_scene(f"{scene_name}_ff", ff_source, fallback, opts)


if __name__ == "__main__":
    main()