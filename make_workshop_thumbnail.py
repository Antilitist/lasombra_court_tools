"""Rebuild Court of Shadows thumbnail: full title + PoD crest corner."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

THUMB = Path(
    r"X:\Users\USER\Documents\Paradox Interactive\Crusader Kings III\mod\lasombra_court\thumbnail.png"
)
POD = Path(r"X:\Users\USER\Pictures\CK3Mod\400px-Podredmarble.png")
OUT = THUMB
BACKUP = THUMB.with_name("thumbnail_pre_workshop_fix.png")

base = Image.open(THUMB).convert("RGBA")
w, h = base.size  # 512x512

# Backup original once if not already backed up
if not BACKUP.exists():
    base.convert("RGB").save(BACKUP, "PNG")
    print(f"Backed up original -> {BACKUP.name}")

# Cover cut-off title with dark atmospheric banner
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for y in range(0, 130):
    t = 1.0 - (y / 130.0)
    alpha = int(215 * (t**0.7))
    od.line([(0, y), (w, y)], fill=(8, 4, 12, alpha))
for y in range(110, 150):
    t = (y - 110) / 40.0
    alpha = int(130 * (1.0 - t))
    od.line([(0, y), (w, y)], fill=(5, 2, 8, alpha))

img = Image.alpha_composite(base, overlay)
draw = ImageDraw.Draw(img)

font_path = r"C:\Windows\Fonts\georgiab.ttf"
font_sub_path = r"C:\Windows\Fonts\georgia.ttf"


def fit_font(text, max_width, start_size, path):
    size = start_size
    while size >= 16:
        f = ImageFont.truetype(path, size)
        bbox = draw.textbbox((0, 0), text, font=f)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if tw <= max_width:
            return f, tw, th
        size -= 1
    f = ImageFont.truetype(path, 16)
    bbox = draw.textbbox((0, 0), text, font=f)
    return f, bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_outlined_text(d, xy, text, font, fill, outline=(0, 0, 0, 230), outline_w=3):
    x, y = xy
    for dx, dy in ((2, 2), (3, 3)):
        d.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 160))
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx * dx + dy * dy <= outline_w * outline_w and (dx or dy):
                d.text((x + dx, y + dy), text, font=font, fill=outline)
    d.text((x, y), text, font=font, fill=fill)


title = "Court of Shadows"
subtitle = "Lasombra Culture & Faith"
pad_x = 24
title_font, tw, th = fit_font(title, w - pad_x * 2, 50, font_path)
sub_font, sw, sh = fit_font(subtitle, w - pad_x * 2, 18, font_sub_path)

title_y = 26
title_x = (w - tw) // 2
draw_outlined_text(
    draw,
    (title_x, title_y),
    title,
    title_font,
    (220, 225, 235, 255),
    outline=(10, 8, 18, 240),
    outline_w=3,
)

sub_y = title_y + th + 4
sub_x = (w - sw) // 2
draw_outlined_text(
    draw,
    (sub_x, sub_y),
    subtitle,
    sub_font,
    (185, 175, 195, 255),
    outline=(0, 0, 0, 200),
    outline_w=2,
)

# PoD crest, bottom-right
pod = Image.open(POD).convert("RGBA")
pod_shield = pod.crop((40, 0, 360, 220))
target_w = 118
ratio = target_w / pod_shield.width
pod_shield = pod_shield.resize(
    (target_w, int(pod_shield.height * ratio)), Image.Resampling.LANCZOS
)

margin = 14
lx = w - pod_shield.width - margin
ly = h - pod_shield.height - margin
plate = Image.new("RGBA", img.size, (0, 0, 0, 0))
pd = ImageDraw.Draw(plate)
pad = 8
pd.rounded_rectangle(
    [lx - pad, ly - pad, lx + pod_shield.width + pad, ly + pod_shield.height + pad],
    radius=10,
    fill=(0, 0, 0, 145),
)
img = Image.alpha_composite(img, plate)
img.paste(pod_shield, (lx, ly), pod_shield)

final = img.convert("RGB")
final.save(OUT, "PNG", optimize=True)
print(f"Wrote {OUT}")
print(f"Title '{title}' width {tw}/{w} (pad {pad_x})")
print(f"PoD crest at ({lx},{ly}) size {pod_shield.size}")
