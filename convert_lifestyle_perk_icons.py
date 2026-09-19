#!/usr/bin/env python3
"""Salon of Night lifestyle art pipeline — symbolic icons matching CK3 conventions.

CK3 finisher perks need TWO 120x120 3-frame sheets (40px/frame): lifestyles_perks/trait_{key}.dds
for the perk tree and traits/{key}.dds for the character trait. Recolor per frame (hue-shift), not flat fill.

Run from mod root:
  python tools/convert_lifestyle_perk_icons.py

Outputs:
  gfx/interface/icons/lifestyles/salon_of_night_lifestyle.dds              480x160 tab (transparent)
  gfx/interface/icons/focuses/*_focus.dds                                    140x140 solid glyphs
  gfx/interface/illustrations/lifestyles_background/salon_of_night_lifestyle.dds
  gfx/interface/icons/lifestyle_tree_backgrounds/{salon_whispers,...}.dds
  gfx/interface/icons/lifestyles_perks/trait_*.dds                           120x120 finisher perks (3x40)
  gfx/interface/icons/traits/{trait_key}.dds                                 120x120 finisher traits (3x40)
"""

from __future__ import annotations

import colorsys
import os
import sys

from PIL import Image, ImageEnhance

MOD = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lasombra_court"))
GFX = os.path.join(MOD, "gfx", "interface")
ICONS = os.path.join(GFX, "icons")

GAME = os.environ.get(
    "CK3_GAME",
    r"D:/Games/steamapps/common/Crusader Kings III/game",
)
POD = os.environ.get(
    "CK3_POD",
    r"D:/Games/steamapps/workshop/content/1158310/2216659254",
)

VANILLA_LIFESTYLES = os.path.join(GAME, "gfx", "interface", "icons", "lifestyles")
VANILLA_FOCUSES = os.path.join(GAME, "gfx", "interface", "icons", "focuses")
VANILLA_TRAITS_LP = os.path.join(GAME, "gfx", "interface", "icons", "lifestyles_perks")
VANILLA_TRAITS = os.path.join(GAME, "gfx", "interface", "icons", "traits")
VANILLA_LIFE_BG = os.path.join(GAME, "gfx", "interface", "illustrations", "lifestyles_background")
VANILLA_TREE_BG = os.path.join(GAME, "gfx", "interface", "icons", "lifestyle_tree_backgrounds")

# Umbral palette
PURPLE = (108, 72, 148)
GOLD = (201, 162, 39)
ASH = (168, 156, 138)
STEEL = (132, 138, 152)
BLOOD = (156, 42, 54)

FOCUS_JOBS = [
    ("salon_whispers_focus.dds", "intrigue_skulduggery_focus.dds", PURPLE),
    ("ash_liturgy_focus.dds", "learning_theology_focus.dds", GOLD),
    ("iron_nocturne_focus.dds", "martial_chivalry_focus.dds", STEEL),
    ("sanguine_court_focus.dds", "stewardship_wealth_focus.dds", BLOOD),
]

# trait_key, lifestyles_perks template, traits/ template, palette
FINISHER_JOBS = [
    ("salon_prince_of_penumbra", "trait_schemer.dds", "schemer.dds", PURPLE),
    ("ash_liturgy_eternal", "trait_theologian.dds", "theologian.dds", GOLD),
    ("nocturne_iron_nocturne", "trait_gallant.dds", "gallant.dds", STEEL),
    ("sanguine_princes_table", "trait_avaricious.dds", "avaricious.dds", BLOOD),
]

# 120x120 lifestyle trait sheets: 3 vertical frames (40px each).
# Frame 1 = available, frame 2 = selected (= character trait icon), frame 3 = muted.
TRAIT_FRAME_STRENGTHS = (0.78, 0.82, 0.72)

TREE_BG_JOBS = [
    ("salon_whispers.dds", "skulduggery.dds", PURPLE, 0.55),
    ("ash_liturgy.dds", "theology.dds", GOLD, 0.45),
    ("iron_nocturne.dds", "chivalry.dds", STEEL, 0.50),
    ("sanguine_court.dds", "wealth.dds", BLOOD, 0.50),
]

# Lifestyle panel illustration (608×1552). Custom art reads better than a double-darkened vanilla tint.
LIFESTYLE_BG_SIZE = (608, 1552)
LIFESTYLE_BG_SOURCE = os.path.join(
    MOD, "tools", "activity_scene_sources", "salon_of_night_lifestyle_bg.jpg"
)


def load_rgba(path: str) -> Image.Image:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGBA")


def write_dds(img: Image.Image, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    print(f"wrote {out_path} ({img.size[0]}x{img.size[1]})")


def solid_glyph_from_template(template_path: str, color: tuple[int, int, int]) -> Image.Image:
    """Single solid-color symbol on transparent background, using vanilla alpha mask."""
    src = load_rgba(template_path)
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    px = src.load()
    opx = out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px[x, y]
            if a > 24:
                opx[x, y] = (*color, a)
    return out


def recolor_preserve_alpha(src: Image.Image, color: tuple[int, int, int], *, strength: float = 1.0) -> Image.Image:
    """Map opaque pixels toward a target hue while keeping the original alpha mask."""
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    px = src.load()
    opx = out.load()
    cr, cg, cb = color
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px[x, y]
            if a <= 8:
                continue
            lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
            lum = max(0.35, min(1.0, lum))
            nr = int(cr * lum * strength + r * (1.0 - strength) * lum)
            ng = int(cg * lum * strength + g * (1.0 - strength) * lum)
            nb = int(cb * lum * strength + b * (1.0 - strength) * lum)
            opx[x, y] = (nr, ng, nb, a)
    return out


def recolor_hue_preserve_value(src: Image.Image, color: tuple[int, int, int], *, strength: float = 1.0) -> Image.Image:
    """Hue-shift toward palette color while preserving per-pixel brightness (value).

    Keeps vanilla's 3-frame contrast: bright available, full selected/trait, muted unavailable.
    """
    target_h, target_s, _target_v = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    px = src.load()
    opx = out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px[x, y]
            if a <= 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            nh = h * (1.0 - strength) + target_h * strength
            ns = s * (1.0 - strength * 0.35) + target_s * (strength * 0.35)
            nr, ng, nb = colorsys.hsv_to_rgb(nh, ns, v)
            opx[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255), a)
    return out


def build_three_frame_lifestyle_icon(template_path: str, color: tuple[int, int, int]) -> Image.Image:
    """Recolor a vanilla 120x120 lifestyle trait sheet frame-by-frame."""
    src = load_rgba(template_path)
    if src.size != (120, 120):
        src = resize_exact(src, (120, 120))
    frame_h = src.height // 3
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    for idx, strength in enumerate(TRAIT_FRAME_STRENGTHS):
        y0 = idx * frame_h
        frame = src.crop((0, y0, src.width, y0 + frame_h))
        tinted = recolor_hue_preserve_value(frame, color, strength=strength)
        out.paste(tinted, (0, y0))
    return out


def crop_cover(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Center-crop to aspect ratio, then resize (matches activity scene pipeline)."""
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


def tint_background(src: Image.Image, color: tuple[int, int, int], strength: float) -> Image.Image:
    rgb = src.convert("RGB")
    tinted = ImageEnhance.Color(rgb).enhance(0.25)
    overlay = Image.new("RGB", src.size, color)
    tinted = Image.blend(tinted, overlay, strength)
    if src.mode == "RGBA":
        tinted = tinted.convert("RGBA")
        tinted.putalpha(src.split()[3])
    return tinted


def resize_exact(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    if img.size == size:
        return img
    return img.resize(size, Image.LANCZOS)


def build_lifestyle_tab_icon() -> None:
    template = os.path.join(VANILLA_LIFESTYLES, "intrigue_lifestyle.dds")
    icon = recolor_preserve_alpha(load_rgba(template), PURPLE, strength=0.92)
    out = os.path.join(ICONS, "lifestyles", "salon_of_night_lifestyle.dds")
    write_dds(icon, out)


def build_focus_icons() -> None:
    out_dir = os.path.join(ICONS, "focuses")
    for out_name, template_name, color in FOCUS_JOBS:
        template = os.path.join(VANILLA_FOCUSES, template_name)
        icon = solid_glyph_from_template(template, color)
        write_dds(icon, os.path.join(out_dir, out_name))


def build_finisher_icons() -> None:
    """Build finisher art as vanilla-style 3-frame 120x120 sheets.

    Perk tree (``[Perk.GetIcon]``):
      ``gfx/interface/icons/lifestyles_perks/trait_{trait_key}.dds``
      Frame 1 = available, frame 2 = selected, frame 3 = muted unavailable.
      Mastery widgets also sample this as 2x60 for taken/untaken states.

    Character trait (``icon = {trait_key}.dds``):
      ``gfx/interface/icons/traits/{trait_key}.dds``
      Uses the same 3-frame sheet; frame 2 (selected) is the owned-trait portrait.
    """
    for trait_key, perk_template_name, trait_template_name, color in FINISHER_JOBS:
        perk_template = os.path.join(VANILLA_TRAITS_LP, perk_template_name)
        if not os.path.isfile(perk_template):
            perk_template = os.path.join(VANILLA_TRAITS, trait_template_name)

        trait_template = os.path.join(VANILLA_TRAITS, trait_template_name)
        if not os.path.isfile(trait_template):
            trait_template = perk_template

        perk_icon = build_three_frame_lifestyle_icon(perk_template, color)
        trait_icon = build_three_frame_lifestyle_icon(trait_template, color)

        write_dds(perk_icon, os.path.join(ICONS, "lifestyles_perks", f"trait_{trait_key}.dds"))
        write_dds(trait_icon, os.path.join(ICONS, "traits", f"{trait_key}.dds"))


def build_lifestyle_background() -> None:
    """Custom Salon of Night panel art (608×1552). Light grade only — source is already high-contrast."""
    tw, th = LIFESTYLE_BG_SIZE
    if os.path.isfile(LIFESTYLE_BG_SOURCE):
        bg = crop_cover(load_rgba(LIFESTYLE_BG_SOURCE), tw, th)
        rgb = bg.convert("RGB")
        rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
        rgb = ImageEnhance.Color(rgb).enhance(1.08)
        rgb = ImageEnhance.Brightness(rgb).enhance(1.10)
        bg = rgb.convert("RGBA")
    else:
        bg = load_rgba(os.path.join(VANILLA_LIFE_BG, "intrigue_lifestyle.dds"))
        if bg.size != (tw, th):
            bg = crop_cover(bg, tw, th)
        bg = recolor_hue_preserve_value(bg, PURPLE, strength=0.38)
        rgb = ImageEnhance.Contrast(bg.convert("RGB")).enhance(1.10)
        rgb = ImageEnhance.Color(rgb).enhance(1.14)
        rgb = ImageEnhance.Brightness(rgb).enhance(0.88)
        bg = rgb.convert("RGBA")

    out = os.path.join(GFX, "illustrations", "lifestyles_background", "salon_of_night_lifestyle.dds")
    write_dds(bg, out)


def build_tree_backgrounds() -> None:
    out_dir = os.path.join(ICONS, "lifestyle_tree_backgrounds")
    for out_name, template_name, color, strength in TREE_BG_JOBS:
        template = os.path.join(VANILLA_TREE_BG, template_name)
        bg = tint_background(load_rgba(template), color, strength)
        bg = ImageEnhance.Brightness(bg).enhance(0.78)
        write_dds(bg, os.path.join(out_dir, out_name))


def main() -> int:
    try:
        build_lifestyle_tab_icon()
        build_focus_icons()
        build_finisher_icons()
        build_lifestyle_background()
        build_tree_backgrounds()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        print("Set CK3_GAME / CK3_POD env vars if install paths differ.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())