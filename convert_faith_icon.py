"""Rebuild Via Tenebrarum faith icons: fill frame, transparent outer vignette only."""
from PIL import Image, ImageEnhance
import numpy as np
import os

SESSION = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", ".grok", "sessions",
                 "C%3A%5CUsers%5CUSER", "019f2379-fcad-7c81-b0d9-c08690713797", "images")
)
if not os.path.isdir(SESSION):
    SESSION = r"F:\Grok\.grok\sessions\C%3A%5CUsers%5CUSER\019f2379-fcad-7c81-b0d9-c08690713797\images"
OUT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "gfx", "interface", "icons", "faith")
)
TARGET = (100, 100)
FILL_RATIO = 0.98

# Distinct Lasombra-themed sources per reform icon slot.
ICON_SOURCES = {
    "via_tenebrarum.dds": "via_tenebrarum_source.jpg",
    "via_tenebrarum_custom.dds": "via_tenebrarum_source.jpg",
    "via_tenebrarum_abyss_custom.dds": "roadoftheabyss.png",
    "via_tenebrarum_mirror_custom.dds": "36.jpg",
    "via_tenebrarum_chalice_custom.dds": "29.jpg",
    "via_tenebrarum_crown_custom.dds": "32.jpg",
}


def luminance(rgb):
    return 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]


def build_alpha(rgb, edge_low=6, edge_mid=18, emblem_floor=210):
    """Fade only the outer black vignette; keep the dark emblem center opaque."""
    lum = luminance(rgb)
    alpha = np.zeros_like(lum, dtype=np.float32)
    fade = (lum - edge_low) / max(edge_mid - edge_low, 1) * 255.0
    alpha = np.clip(fade, 0, 255)
    alpha[lum >= edge_mid] = 255.0
    interior = (lum >= edge_low) & (lum < edge_mid)
    alpha[interior] = np.maximum(alpha[interior], emblem_floor)
    return alpha.astype(np.uint8)


def lift_emblem_rgb(rgb):
    """Boost dark interior pixels so the center reads on faith UI backgrounds."""
    lum = luminance(rgb)
    out = rgb.copy()
    mask = (lum >= 6) & (lum < 55)
    if np.any(mask):
        lifted = rgb[mask] * 2.1 + 28.0
        out[mask] = np.clip(lifted, 0, 255)
    return out.astype(np.uint8)


def crop_to_alpha(img, threshold=24):
    arr = np.array(img)
    ys, xs = np.where(arr[:, :, 3] > threshold)
    if len(xs) == 0:
        return img
    pad = 2
    left = max(0, xs.min() - pad)
    top = max(0, ys.min() - pad)
    right = min(img.width, xs.max() + pad + 1)
    bottom = min(img.height, ys.max() + pad + 1)
    return img.crop((left, top, right, bottom))


def fit_on_canvas(img, size, fill_ratio):
    tw, th = size
    max_w = int(tw * fill_ratio)
    max_h = int(th * fill_ratio)
    img.thumbnail((max_w, max_h), Image.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (tw - img.width) // 2
    y = (th - img.height) // 2
    canvas.paste(img, (x, y), img)
    return canvas


def process_source(src_path):
    src = Image.open(src_path).convert("RGB")
    rgb = np.array(src).astype(np.float32)
    rgb_arr = lift_emblem_rgb(rgb)
    alpha = build_alpha(rgb_arr.astype(np.float32))
    rgba = np.dstack([rgb_arr, alpha])
    img = Image.fromarray(rgba, "RGBA")

    rgb_img = Image.fromarray(rgba[:, :, :3], "RGB")
    rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.18)
    rgb_img = ImageEnhance.Color(rgb_img).enhance(1.1)
    rgb_arr = np.array(rgb_img)
    alpha_arr = rgba[:, :, 3]
    img = Image.fromarray(np.dstack([rgb_arr, alpha_arr]), "RGBA")

    img = crop_to_alpha(img)
    return fit_on_canvas(img, TARGET, FILL_RATIO)


def main():
    tools_dir = os.path.dirname(__file__)
    os.makedirs(OUT_DIR, exist_ok=True)
    for out_name, src_name in ICON_SOURCES.items():
        src_path = os.path.join(tools_dir, src_name)
        if not os.path.exists(src_path):
            src_path = os.path.join(SESSION, src_name)
        if not os.path.exists(src_path):
            raise FileNotFoundError(src_path)
        img = process_source(src_path)
        out = os.path.join(OUT_DIR, out_name)
        img.save(out)
        print("wrote", out, img.size, "mode", img.mode, "from", src_name)


if __name__ == "__main__":
    main()