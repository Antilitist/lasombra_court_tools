"""Umbral council panel backgrounds and council task icons for CK3."""
from PIL import Image, ImageChops, ImageEnhance, ImageDraw, ImageFilter
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(TOOLS, "..", "lasombra_court"))
SCENE_SIZE = (1592, 848)
TASK_ICON_SIZE = (140, 140)
TASK_ICON_INNER = 116

COUNCIL_BACKGROUNDS = {
    "lasombra_court_council_curator": (
        "source_51.jpg",
        {"contrast": 1.1, "color": 1.12, "tint": (35, 8, 45), "tint_strength": 0.18},
    ),
    "lasombra_court_council_legate": (
        "source_52.jpg",
        {"contrast": 1.12, "color": 1.0, "tint": (30, 5, 8), "tint_strength": 0.2},
    ),
}

# Unique painted icons — one focal subject per Umbral council task.
COUNCIL_TASK_ICON_SOURCES = {
    "lasombra_court_warden_night_watch_task": "source_task_warden_night_watch.jpg",
    "lasombra_court_warden_penumbra_knights_task": "source_task_warden_penumbra_knights.jpg",
    "lasombra_court_warden_obscure_demesne_task": "source_task_warden_obscure_demesne.jpg",
    "lasombra_court_legate_preach_task": "source_task_legate_preach.jpg",
    "lasombra_court_legate_blood_absolution_task": "source_task_legate_blood_absolution.jpg",
    "lasombra_court_legate_sanctify_chapels_task": "source_task_legate_sanctify_chapels.jpg",
    "lasombra_court_curator_fan_flame_task": "source_task_curator_fan_flame.jpg",
    "lasombra_court_curator_bind_carnal_oath_task": "source_task_curator_bind_carnal_oath.jpg",
    "lasombra_court_curator_saturate_night_task": "source_task_curator_saturate_night.jpg",
    "lasombra_court_curator_tempt_heart_task": "source_task_curator_tempt_heart.jpg",
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
    return apply_tint(rgb, opts.get("tint", (20, 10, 30)), opts.get("tint_strength", 0.2))


def circular_mask(size, inset=1):
    w, h = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((inset, inset, w - inset - 1, h - inset - 1), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.5))


def remove_near_white_background(img, threshold=235, softness=30):
    """Fade out bright white JPG mattes."""
    img = img.convert("RGBA")
    pixels = list(img.getdata())
    cleaned = []
    for r, g, b, a in pixels:
        brightness = (r + g + b) / 3.0
        if brightness >= threshold and min(r, g, b) >= threshold - 20:
            fade = max(0.0, min(1.0, (brightness - (threshold - softness)) / softness))
            new_a = int(a * (1.0 - fade))
            cleaned.append((r, g, b, new_a))
        else:
            cleaned.append((r, g, b, a))
    img.putdata(cleaned)
    return img


def sample_edge_background_color(img):
    width, height = img.size
    samples = []
    step = max(1, min(width, height) // 12)
    for x in range(0, width, step):
        samples.append(img.getpixel((x, 0))[:3])
        samples.append(img.getpixel((x, height - 1))[:3])
    for y in range(0, height, step):
        samples.append(img.getpixel((0, y))[:3])
        samples.append(img.getpixel((width - 1, y))[:3])
    return (
        sum(color[0] for color in samples) // len(samples),
        sum(color[1] for color in samples) // len(samples),
        sum(color[2] for color in samples) // len(samples),
    )


def remove_matte_background_flood(img, tolerance=38):
    """Strip neutral/gray AI matte backgrounds via edge flood fill."""
    img = img.convert("RGBA")
    width, height = img.size
    seeds = {
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
    }
    step = max(1, min(width, height) // 12)
    for x in range(0, width, step):
        seeds.add((x, 0))
        seeds.add((x, height - 1))
    for y in range(0, height, step):
        seeds.add((0, y))
        seeds.add((width - 1, y))

    draw = ImageDraw.Draw(img)
    for seed in seeds:
        if 0 <= seed[0] < width and 0 <= seed[1] < height and img.getpixel(seed)[3] > 0:
            ImageDraw.floodfill(img, seed, (0, 0, 0, 0), thresh=tolerance)
    return img


def remove_neutral_matte_fringe(img, tolerance=62):
    """Remove leftover neutral mist or gray boxes AI leaves inside the subject."""
    img = img.convert("RGBA")
    background = sample_edge_background_color(img)
    pixels = list(img.getdata())
    cleaned = []
    for red, green, blue, alpha in pixels:
        if alpha < 1:
            cleaned.append((red, green, blue, alpha))
            continue

        distance = (
            (red - background[0]) ** 2
            + (green - background[1]) ** 2
            + (blue - background[2]) ** 2
        ) ** 0.5
        saturation = max(red, green, blue) - min(red, green, blue)
        brightness = (red + green + blue) / 3.0
        fade = 0.0

        if distance <= tolerance and saturation <= 42:
            fade = max(0.0, 1.0 - distance / tolerance)
        elif brightness >= 165 and saturation <= 34:
            fade = min(1.0, max(0.0, (brightness - 158) / 72))

        if fade > 0:
            cleaned.append((red, green, blue, int(alpha * (1.0 - fade))))
        else:
            cleaned.append((red, green, blue, alpha))

    img.putdata(cleaned)
    return img


def remove_icon_background(img):
    """Remove white or gray AI-generated mattes before circular masking."""
    img = remove_matte_background_flood(img, tolerance=42)
    img = remove_neutral_matte_fringe(img, tolerance=62)
    img = remove_near_white_background(img, threshold=210, softness=48)
    return img


def apply_circular_alpha(img, inset=1):
    mask = circular_mask(img.size, inset=inset)
    red, green, blue, alpha = img.split()
    alpha = ImageChops.multiply(alpha, mask)
    return Image.merge("RGBA", (red, green, blue, alpha))


def make_task_icon(src_path):
    src = Image.open(src_path).convert("RGBA")
    src = remove_icon_background(src)
    src = crop_cover(src, TASK_ICON_INNER, TASK_ICON_INNER)
    src = apply_circular_alpha(src, inset=2)
    src = ImageEnhance.Contrast(src).enhance(1.12)
    src = ImageEnhance.Color(src).enhance(1.06)
    src = ImageEnhance.Sharpness(src).enhance(1.35)

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

    inset = (TASK_ICON_SIZE[0] - TASK_ICON_INNER) // 2
    canvas.paste(src, (inset, inset), src)
    return canvas.filter(ImageFilter.UnsharpMask(radius=1.2, percent=160, threshold=1))


def write_backgrounds():
    out_dir = os.path.join(MOD, "gfx", "interface", "illustrations", "event_scenes")
    os.makedirs(out_dir, exist_ok=True)
    for name, (src_name, opts) in COUNCIL_BACKGROUNDS.items():
        src_path = os.path.join(TOOLS, src_name)
        out_path = os.path.join(out_dir, f"{name}.dds")
        img = Image.open(src_path).convert("RGBA")
        img = crop_cover(img, *SCENE_SIZE)
        out = enhance_scene(img, opts)
        out.save(out_path)
        print(f"background: {name}")


def write_council_task_icons():
    out_dir = os.path.join(MOD, "gfx", "interface", "icons", "council_task_types")
    os.makedirs(out_dir, exist_ok=True)
    for task_id, src_name in COUNCIL_TASK_ICON_SOURCES.items():
        src_path = os.path.join(TOOLS, src_name)
        out_path = os.path.join(out_dir, f"{task_id}.dds")
        icon = make_task_icon(src_path)
        icon.save(out_path)
        print(f"task icon: {task_id}")


def main():
    write_backgrounds()
    write_council_task_icons()


if __name__ == "__main__":
    main()