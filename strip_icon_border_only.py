"""Remove only the outer purple square frame from Via Tenebrarum faith icons.

Does not crop, resize, or reprocess from source — edits alpha in-place on the
existing 100x100 icon so the emblem, crown, and blood drip stay untouched.
"""
from PIL import Image
import numpy as np
import os

MOD = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lasombra_court"))
ICON_DIR = os.path.join(MOD, "gfx", "interface", "icons", "faith")
TARGETS = ("via_tenebrarum.dds", "via_tenebrarum_custom.dds")
BORDER_THICKNESS = 6


def is_outer_frame_pixel(rgb, alpha):
    """Bright glowing purple square border — not dark emblem swirls."""
    r = rgb[..., 0]
    g = rgb[..., 1]
    b = rgb[..., 2]
    return (
        (alpha > 120)
        & (r > 85)
        & (b > 100)
        & (g < 125)
        & ((r + b) > (g * 2.2 + 50))
    )


def strip_border(img):
    arr = np.array(img.convert("RGBA"), copy=True)
    h, w = arr.shape[:2]
    rgb = arr[:, :, :3].astype(np.float32)
    alpha = arr[:, :, 3].astype(np.float32)
    frame = is_outer_frame_pixel(rgb, alpha)

    border = np.zeros((h, w), dtype=bool)
    t = BORDER_THICKNESS
    border[:t, :] = True
    border[h - t :, :] = True
    border[:, :t] = True
    border[:, w - t :] = True

    kill = border & frame
    alpha[kill] = 0

    # Full-width purple bars (top/bottom of the decorative square)
    for y in range(h):
        row = frame[y] & (alpha[y] > 120)
        if row.sum() >= w * 0.55:
            alpha[y, row] = 0

    arr[:, :, 3] = alpha.astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def main():
    for name in TARGETS:
        path = os.path.join(ICON_DIR, name)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        out = strip_border(Image.open(path))
        out.save(path)
        print("stripped border:", path)


if __name__ == "__main__":
    main()