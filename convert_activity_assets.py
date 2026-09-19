"""Court of Shadows activity icons — round map pins and option category art."""
import importlib.util
import os
import shutil
import tempfile
from PIL import Image

from dds_compress import (
    finalize_activity_header_dds,
    finalize_activity_icon_dds,
    finalize_activity_title_icon_dds,
)

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(TOOLS, "..", "lasombra_court"))

ACTIVITIES = (
    "activity_lasombra_court_black_chapel_procession",
)
# Veiled Pursuit art is built by convert_veiled_pursuit_assets.py (custom source).

ACTIVITY_ICON_SIZE = (80, 80)
ACTIVITY_TITLE_ICON_SIZE = (164, 164)
CATEGORY_ICON_SIZE = (96, 120)
HEADER_SIZE = (1100, 440)

TEMPT_HEART_SRC = os.path.join(TOOLS, "source_task_curator_tempt_heart.jpg")
EVENT_SCENE_SRC = os.path.join(
    MOD, "gfx", "interface", "illustrations", "event_scenes", "lasombra_court_umbral_orgy.dds"
)


def load_council_converter():
    path = os.path.join(TOOLS, "convert_umbral_council_assets.py")
    spec = importlib.util.spec_from_file_location("convert_umbral_council_assets", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save_activity_icon(img, path, finalize=finalize_activity_icon_dds):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".dds", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        img.save(tmp_path)
        finalize(tmp_path)
        shutil.move(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    print("wrote", path, img.size)


def save_header_background(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".dds", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        img.save(tmp_path)
        finalize_activity_header_dds(tmp_path)
        shutil.move(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    print("wrote", path, img.size)


def make_activity_map_icon(converter):
    """Round, transparent-edged icon for map planner pins."""
    task_icon = converter.make_task_icon(TEMPT_HEART_SRC)
    return task_icon.resize(ACTIVITY_ICON_SIZE, Image.LANCZOS)


def make_activity_title_icon(converter):
    """Larger round icon for the running-activity window title bar."""
    task_icon = converter.make_task_icon(TEMPT_HEART_SRC)
    return task_icon.resize(ACTIVITY_TITLE_ICON_SIZE, Image.LANCZOS)


def make_option_category_icon(converter):
    """Sidebar option-category button art (vanilla hunt icons are 96x120)."""
    task_icon = converter.make_task_icon(TEMPT_HEART_SRC)
    canvas = Image.new("RGBA", CATEGORY_ICON_SIZE, (0, 0, 0, 0))
    scaled = task_icon.resize((88, 88), Image.LANCZOS)
    inset_x = (CATEGORY_ICON_SIZE[0] - scaled.size[0]) // 2
    inset_y = (CATEGORY_ICON_SIZE[1] - scaled.size[1]) // 2 - 4
    canvas.paste(scaled, (inset_x, inset_y), scaled)
    return canvas


def make_header_background():
    img = Image.open(EVENT_SCENE_SRC).convert("RGBA")
    img = img.resize(HEADER_SIZE, Image.LANCZOS)
    return img


def main():
    converter = load_council_converter()
    map_icon = make_activity_map_icon(converter)
    title_icon = make_activity_title_icon(converter)
    category_icon = make_option_category_icon(converter)
    header = make_header_background()

    activity_icon_dir = os.path.join(MOD, "gfx", "interface", "icons", "activities")
    category_icon_dir = os.path.join(MOD, "gfx", "interface", "icons", "activity_option_categories")
    header_dir = os.path.join(MOD, "gfx", "interface", "illustrations", "activity_header_backgrounds")

    for key in ACTIVITIES:
        save_activity_icon(map_icon, os.path.join(activity_icon_dir, f"{key}.dds"))
        save_activity_icon(
            title_icon,
            os.path.join(activity_icon_dir, f"{key}_header.dds"),
            finalize=finalize_activity_title_icon_dds,
        )
        save_header_background(header, os.path.join(header_dir, f"{key}.dds"))

    save_activity_icon(category_icon, os.path.join(category_icon_dir, "lasombra_court_rite_scale.dds"))


if __name__ == "__main__":
    main()