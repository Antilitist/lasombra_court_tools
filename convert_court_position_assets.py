"""Generate Umbral court position backgrounds, type icons, and task icons for CK3."""
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os

SESSION = r"X:\Users\USER\.grok\sessions\C%3A%5CUsers%5CUSER\019f2379-fcad-7c81-b0d9-c08690713797\images"
MOD = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lasombra_court"))
SCENE_SIZE = (1592, 848)
TASK_ICON_SIZE = (140, 140)
POSITION_ICON_SIZE = (70, 70)

BACKGROUNDS = {
    "lasombra_court_cp_salon": ("46.jpg", {"contrast": 1.1, "color": 1.05, "tint": (30, 10, 40)}),
    "lasombra_court_cp_saturnalia": ("50.jpg", {"contrast": 1.12, "color": 1.15, "tint": (50, 15, 20)}),
    "lasombra_court_cp_eclipse": ("49.jpg", {"contrast": 1.08, "color": 1.0, "tint": (10, 15, 45)}),
    "lasombra_court_cp_confessor": ("44.jpg", {"contrast": 1.1, "color": 0.95, "tint": (35, 8, 8)}),
    "lasombra_court_cp_whisper": ("48.jpg", {"contrast": 1.1, "color": 0.9, "tint": (15, 20, 30)}),
    "lasombra_court_cp_herd": ("45.jpg", {"contrast": 1.08, "color": 1.05, "tint": (25, 12, 35)}),
    "lasombra_court_cp_thrall": ("41.jpg", {"contrast": 1.15, "color": 0.95, "tint": (20, 20, 25)}),
    "lasombra_court_cp_arbiter": ("47.jpg", {"contrast": 1.12, "color": 0.9, "tint": (40, 5, 5)}),
}

POSITION_ICONS = {
    "lasombra_court_shadow_harem_keeper_court_position": "gfx/interface/icons/faith_doctrines/lasombra_tenet_shadow_harem.dds",
    "lasombra_court_saturnalia_master_court_position": "gfx/interface/icons/faith_doctrines/lasombra_tenet_saturnalia_tenebris.dds",
    "lasombra_court_eclipse_cupbearer_court_position": "gfx/interface/icons/faith_doctrines/lasombra_tenet_chalice_eclipse.dds",
    "lasombra_court_blood_confessor_court_position": "gfx/interface/icons/traits/lasombra_court_ash_liturgist.dds",
    "lasombra_court_amici_whisper_court_position": "gfx/interface/icons/faith_doctrines/lasombra_tenet_amici_noctis.dds",
    "lasombra_court_herd_binder_court_position": "gfx/interface/icons/faith_doctrines/lasombra_tenet_veiled_hunger.dds",
    "lasombra_court_thrall_master_court_position": "gfx/interface/icons/faith_doctrines/lasombra_tenet_iron_nocturne.dds",
    "lasombra_court_blood_arbiter_court_position": "gfx/interface/icons/traits/lasombra_court_blood_arbiter.dds",
}

TASK_ICONS = {
    "lasombra_court_harem_keeper_curate_salon_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_shadow_harem.dds",
    "lasombra_court_harem_keeper_scout_favorite_task": "gfx/interface/icons/traits/lasombra_court_shadow_consort.dds",
    "lasombra_court_saturnalia_prepare_chapel_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_ash_liturgy.dds",
    "lasombra_court_saturnalia_kindle_revelry_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_saturnalia_tenebris.dds",
    "lasombra_court_eclipse_serve_draught_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_chalice_eclipse.dds",
    "lasombra_court_eclipse_commune_court_task": "gfx/interface/icons/faith/via_tenebrarum_chalice_custom.dds",
    "lasombra_court_confessor_hear_confession_task": "gfx/interface/icons/traits/lasombra_court_ash_liturgist.dds",
    "lasombra_court_confessor_grant_indulgence_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_blood_absolution.dds",
    "lasombra_court_whisper_carry_word_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_amici_noctis.dds",
    "lasombra_court_whisper_map_network_task": "gfx/interface/icons/traits/lasombra_court_friend_of_night.dds",
    "lasombra_court_herd_binder_tend_flock_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_veiled_hunger.dds",
    "lasombra_court_herd_binder_recruit_salon_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_sanguine_bonds.dds",
    "lasombra_court_thrall_master_train_thralls_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_iron_nocturne.dds",
    "lasombra_court_thrall_master_bind_thrall_task": "gfx/interface/icons/traits/lasombra_court_living_shadow.dds",
    "lasombra_court_arbiter_proclaim_sentence_task": "gfx/interface/icons/traits/lasombra_court_blood_arbiter.dds",
    "lasombra_court_arbiter_sanction_devouring_task": "gfx/interface/icons/faith_doctrines/lasombra_tenet_trophy_skulls.dds",
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


def apply_tint(img, tint_rgb, strength=0.22):
    tint = Image.new("RGB", img.size, tint_rgb)
    base = img.convert("RGB")
    return Image.blend(base, tint, strength).convert("RGBA")


def enhance_scene(img, opts):
    rgb = img.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(opts.get("contrast", 1.08))
    rgb = ImageEnhance.Color(rgb).enhance(opts.get("color", 1.05))
    out = apply_tint(rgb, opts.get("tint", (20, 10, 30)), opts.get("tint_strength", 0.2))
    return out


def circular_mask(size, inset=2):
    w, h = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((inset, inset, w - inset - 1, h - inset - 1), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.6))


def make_position_icon(src_path):
    src = Image.open(src_path).convert("RGBA")
    src = crop_cover(src, *POSITION_ICON_SIZE)
    src = ImageEnhance.Contrast(src).enhance(1.08)
    src = ImageEnhance.Color(src).enhance(1.05)
    src.putalpha(circular_mask(POSITION_ICON_SIZE))
    return src.filter(ImageFilter.UnsharpMask(radius=0.8, percent=120, threshold=2))


def make_task_icon(src_path):
    src = Image.open(src_path).convert("RGBA")
    src = crop_cover(src, 100, 100)

    canvas = Image.new("RGBA", TASK_ICON_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    cx, cy = TASK_ICON_SIZE[0] // 2, TASK_ICON_SIZE[1] // 2
    for radius, alpha in [(68, 220), (64, 255), (58, 180)]:
        draw.ellipse(
            (cx - radius, cy - radius, cx + radius, cy + radius),
            fill=(18, 10, 24, alpha),
        )
    draw.ellipse(
        (cx - 62, cy - 62, cx + 62, cy + 62),
        outline=(120, 90, 45, 255),
        width=3,
    )
    draw.ellipse(
        (cx - 58, cy - 58, cx + 58, cy + 58),
        outline=(60, 45, 25, 200),
        width=2,
    )

    canvas.paste(src, (20, 20), src)
    canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1, percent=130, threshold=2))
    return canvas


def write_backgrounds():
    out_dir = os.path.join(MOD, "gfx", "interface", "illustrations", "event_scenes")
    os.makedirs(out_dir, exist_ok=True)
    for name, (src_name, opts) in BACKGROUNDS.items():
        src_path = os.path.join(SESSION, src_name)
        out_path = os.path.join(out_dir, f"{name}.dds")
        img = Image.open(src_path).convert("RGBA")
        img = crop_cover(img, *SCENE_SIZE)
        out = enhance_scene(img, opts)
        out.save(out_path)
        print(f"background: {name}")


def write_position_icons():
    out_dir = os.path.join(MOD, "gfx", "interface", "icons", "court_position_types")
    os.makedirs(out_dir, exist_ok=True)
    for position_id, rel_src in POSITION_ICONS.items():
        src_path = os.path.join(MOD, rel_src.replace("/", os.sep))
        out_path = os.path.join(out_dir, f"{position_id}.dds")
        icon = make_position_icon(src_path)
        icon.save(out_path)
        print(f"position icon: {position_id}")


def write_task_icons():
    out_dir = os.path.join(MOD, "gfx", "interface", "icons", "court_position_task_types")
    os.makedirs(out_dir, exist_ok=True)
    for task_id, rel_src in TASK_ICONS.items():
        src_path = os.path.join(MOD, rel_src.replace("/", os.sep))
        out_path = os.path.join(out_dir, f"{task_id}.dds")
        icon = make_task_icon(src_path)
        icon.save(out_path)
        print(f"task icon: {task_id}")


def main():
    write_backgrounds()
    write_position_icons()
    write_task_icons()


if __name__ == "__main__":
    main()