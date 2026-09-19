"""Craft Nox Nuda tenet icon: artful female silhouette on night field, 260x400."""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import math
import os
import numpy as np

W, H = 520, 800
OUT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "gfx", "interface", "icons", "faith_doctrines")
)
PREVIEW = os.path.join(os.path.dirname(__file__), "source_tenet_nox_nuda.png")
DDS = os.path.join(OUT_DIR, "lasombra_tenet_nox_nuda.dds")


def make_bg():
    img = Image.new("RGBA", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        r = int(6 + 10 * t)
        g = int(4 + 8 * t)
        b = int(16 + 36 * t)
        for x in range(W):
            nx = (x - W / 2) / (W / 2)
            ny = (y - H * 0.4) / (H / 2)
            edge = min(1.0, math.sqrt(nx * nx + ny * ny) * 0.55)
            f = 1.0 - 0.35 * edge
            px[x, y] = (int(r * f), int(g * f), int(b * f), 255)
    return img


def paint_blob(mask, cx, cy, rx, ry, strength=1.0):
    a = np.array(mask, dtype=np.float32)
    ys, xs = np.ogrid[:H, :W]
    e = ((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2
    add = np.clip(1.0 - e, 0, 1) ** 1.35 * 255 * strength
    a = np.maximum(a, add)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "L")


def main():
    mask = Image.new("L", (W, H), 0)
    cx = W * 0.5
    head_y = H * 0.17
    u = H * 0.054

    # Head / neck
    mask = paint_blob(mask, cx, head_y + 0.55 * u, 0.70 * u, 0.92 * u)
    mask = paint_blob(mask, cx, head_y + 1.5 * u, 0.26 * u, 0.42 * u)
    # Shoulders / torso / waist / hips — one continuous feminine form
    mask = paint_blob(mask, cx, head_y + 2.35 * u, 1.50 * u, 0.50 * u)
    mask = paint_blob(mask, cx, head_y + 3.25 * u, 1.18 * u, 1.05 * u)
    mask = paint_blob(mask, cx, head_y + 4.55 * u, 0.80 * u, 0.80 * u)
    mask = paint_blob(mask, cx, head_y + 5.85 * u, 1.32 * u, 0.95 * u)
    # Legs
    mask = paint_blob(mask, cx - 0.42 * u, head_y + 7.15 * u, 0.52 * u, 1.05 * u)
    mask = paint_blob(mask, cx + 0.42 * u, head_y + 7.15 * u, 0.52 * u, 1.05 * u)
    mask = paint_blob(mask, cx - 0.48 * u, head_y + 8.95 * u, 0.40 * u, 1.35 * u)
    mask = paint_blob(mask, cx + 0.52 * u, head_y + 9.0 * u, 0.40 * u, 1.40 * u)
    mask = paint_blob(mask, cx - 0.52 * u, head_y + 10.45 * u, 0.52 * u, 0.26 * u)
    mask = paint_blob(mask, cx + 0.62 * u, head_y + 10.5 * u, 0.55 * u, 0.26 * u)
    # Arms
    mask = paint_blob(mask, cx - 1.50 * u, head_y + 3.45 * u, 0.36 * u, 1.45 * u)
    mask = paint_blob(mask, cx - 1.65 * u, head_y + 5.15 * u, 0.30 * u, 1.05 * u)
    mask = paint_blob(mask, cx + 1.40 * u, head_y + 3.55 * u, 0.34 * u, 1.50 * u)
    mask = paint_blob(mask, cx + 1.45 * u, head_y + 5.25 * u, 0.28 * u, 1.0 * u)

    mask = mask.filter(ImageFilter.GaussianBlur(3.2))
    arr = np.array(mask, dtype=np.float32)
    arr = np.clip((arr - 38) * 1.45, 0, 255)
    mask = Image.fromarray(arr.astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(1.1))

    img = make_bg()

    # Violet rim
    rim_mask = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(7))
    ra = np.zeros((H, W, 4), dtype=np.uint8)
    rm = np.array(rim_mask)
    body = np.array(mask)
    glow = np.clip(rm.astype(np.int16) - body.astype(np.int16) * 0.85, 0, 255).astype(np.uint8)
    ra[:, :, 0] = 145
    ra[:, :, 1] = 120
    ra[:, :, 2] = 210
    ra[:, :, 3] = (glow.astype(np.float32) * 0.55).astype(np.uint8)
    img = Image.alpha_composite(img, Image.fromarray(ra, "RGBA"))

    # Solid silhouette
    ba = np.zeros((H, W, 4), dtype=np.uint8)
    ba[:, :, 0] = 3
    ba[:, :, 1] = 2
    ba[:, :, 2] = 8
    ba[:, :, 3] = np.array(mask)
    img = Image.alpha_composite(img, Image.fromarray(ba, "RGBA"))

    # Silver edge
    exp = mask.filter(ImageFilter.MaxFilter(3))
    edge_a = np.clip(
        np.array(exp, dtype=np.int16) - np.array(mask, dtype=np.int16), 0, 255
    ).astype(np.uint8)
    ea = np.zeros((H, W, 4), dtype=np.uint8)
    ea[:, :, 0] = 170
    ea[:, :, 1] = 175
    ea[:, :, 2] = 210
    ea[:, :, 3] = edge_a
    edge = Image.fromarray(ea, "RGBA").filter(ImageFilter.GaussianBlur(0.5))
    img = Image.alpha_composite(img, edge)

    # Crescent moon
    moon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(moon)
    mx, my, mr = int(W * 0.74), int(H * 0.16), 42
    md.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(195, 200, 230, 100))
    md.ellipse(
        [mx - mr + 16, my - mr - 10, mx + mr + 16, my + mr - 10], fill=(8, 6, 18, 255)
    )
    img = Image.alpha_composite(img, moon.filter(ImageFilter.GaussianBlur(1.5)))

    # Corner ornaments
    draw = ImageDraw.Draw(img)
    c = (100, 80, 140, 150)
    draw.arc([18, 18, 88, 88], 180, 270, fill=c, width=2)
    draw.arc([W - 88, 18, W - 18, 88], 270, 360, fill=c, width=2)
    draw.arc([18, H - 88, 88, H - 18], 90, 180, fill=c, width=2)
    draw.arc([W - 88, H - 88, W - 18, H - 18], 0, 90, fill=c, width=2)

    # Ground mist
    mist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(mist).ellipse(
        [W * 0.1, H * 0.78, W * 0.9, H * 1.05], fill=(50, 25, 80, 50)
    )
    img = Image.alpha_composite(img, mist.filter(ImageFilter.GaussianBlur(25)))

    out = img.resize((260, 400), Image.LANCZOS)
    rgb = ImageEnhance.Contrast(out.convert("RGB")).enhance(1.1)
    rgb = ImageEnhance.Color(rgb).enhance(1.05)
    final = rgb.convert("RGBA")

    os.makedirs(OUT_DIR, exist_ok=True)
    final.save(PREVIEW)
    final.save(DDS)
    print("wrote", PREVIEW)
    print("wrote", DDS, final.size)


if __name__ == "__main__":
    main()
