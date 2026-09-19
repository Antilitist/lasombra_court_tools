"""Build Legacy of the Penumbra dynasty icon and panoramic track art."""
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageStat
import numpy as np
import os

SESSION = r"X:\Users\USER\.grok\sessions\C%3A%5CUsers%5CUSER\019f2379-fcad-7c81-b0d9-c08690713797\images"
MOD = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lasombra_court"))

TRACK_SIZE = (4216, 368)
ICON_SIZE = (140, 140)
SEGMENTS = 5
SEG_WIDTH = TRACK_SIZE[0] // SEGMENTS
OVERLAP = 176
TARGET_MEAN = 52.0

# Flirty → sensual → orgy escalation, left to right across legacy tiers.
SEGMENT_SOURCES = [
    ("10.jpg", 0.32),   # Salon of Whispers — stolen kiss in the candlelit corridor
    ("27.jpg", 0.22),   # Ash Liturgy — roses, goblet, bodies leaning close
    ("45.jpg", 0.35),   # Courts of Flesh — reclining consorts and bare shoulders
    ("50.jpg", 0.55),   # Iron Nocturne — Saturnalia revel sprawled on the floor
    ("28.jpg", 0.46),   # Penumbra Eternal — entangled climax of the black mass
]

def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def crop_cover(img, tw, th, bias=0.5):
    w, h = img.size
    target_ratio = tw / th
    src_ratio = w / h
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = int((w - new_w) * bias)
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = int((h - new_h) * bias)
        img = img.crop((0, top, w, top + new_h))
    return img.resize((tw, th), Image.LANCZOS)


def brighten_legacy(img, flirt_boost=False):
    rgb = img.convert("RGB")
    rgb = ImageEnhance.Brightness(rgb).enhance(1.46)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.1)
    color_boost = 1.28 if flirt_boost else 1.2
    rgb = ImageEnhance.Color(rgb).enhance(color_boost)
    warm = Image.new("RGB", rgb.size, (92, 38, 52) if flirt_boost else (78, 42, 28))
    rgb = Image.blend(rgb, warm, 0.12 if flirt_boost else 0.1)
    out = rgb.convert("RGBA")
    mean = sum(ImageStat.Stat(out.convert("RGB")).mean) / 3.0
    if mean < TARGET_MEAN:
        lift = TARGET_MEAN / max(mean, 1.0)
        rgb = ImageEnhance.Brightness(out.convert("RGB")).enhance(min(lift, 1.22))
        out = rgb.convert("RGBA")
    return out.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=3))


def load_segment(src_name, bias, flirt_boost=False):
    path = os.path.join(SESSION, src_name)
    img = Image.open(path).convert("RGBA")
    return brighten_legacy(crop_cover(img, SEG_WIDTH, TRACK_SIZE[1], bias=bias), flirt_boost=flirt_boost)


def lift_trailing_edge(seg, seg_index):
    """Brighten the right margin on early tiers so seams never read as black bars."""
    if seg_index >= SEGMENTS - 1:
        return seg
    out = seg.copy()
    lift_cols = OVERLAP + 64
    start = SEG_WIDTH - lift_cols
    peak = 1.62 if seg_index == 2 else 1.42
    ramp = np.linspace(1.0, peak, lift_cols, dtype=np.float64)
    out[:, start:] *= ramp[np.newaxis, :, np.newaxis]
    return np.clip(out, 0, 255)


def compose_track():
    segments = []
    for index, (src, bias) in enumerate(SEGMENT_SOURCES):
        seg = np.array(load_segment(src, bias, flirt_boost=True).convert("RGB"), dtype=np.float64)
        segments.append(lift_trailing_edge(seg, index))

    height, width = TRACK_SIZE[1], TRACK_SIZE[0]
    x = np.arange(width, dtype=np.int32)
    col = np.minimum(x // SEG_WIDTH, SEGMENTS - 1)
    local_x = np.minimum(x - col * SEG_WIDTH, SEG_WIDTH - 1)
    result = np.zeros((height, width, 3), dtype=np.float64)

    for c in range(SEGMENTS):
        col_mask = col == c
        if not np.any(col_mask):
            continue
        xs = np.where(col_mask)[0]
        lx = local_x[col_mask]
        blend_mask = (c > 0) & (lx < OVERLAP)
        solid_mask = ~blend_mask

        if np.any(solid_mask):
            sx = xs[solid_mask]
            result[:, sx] = segments[c][:, lx[solid_mask]]

        if np.any(blend_mask):
            bx = xs[blend_mask]
            blx = lx[blend_mask]
            t = smoothstep(blx / OVERLAP)
            prev_x = SEG_WIDTH - OVERLAP + blx
            left = segments[c - 1][:, prev_x]
            right = segments[c][:, blx]
            result[:, bx] = left * (1.0 - t[:, np.newaxis]) + right * t[:, np.newaxis]

    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")


def make_dynasty_icon():
    """PoD Lasombra legacy icon with the crown recolored dark purple."""
    pod_icon = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "..",
            "..",
            "Games",
            "steamapps",
            "workshop",
            "content",
            "1158310",
            "2216659254",
            "gfx",
            "interface",
            "icons",
            "dynasty",
            "lasombra_legacy_track.dds",
        )
    )
    if not os.path.isfile(pod_icon):
        pod_icon = r"D:\Games\steamapps\workshop\content\1158310\2216659254\gfx\interface\icons\dynasty\lasombra_legacy_track.dds"

    crown_purple = np.array([72, 28, 98], dtype=np.uint8)
    icon = Image.open(pod_icon).convert("RGBA")
    arr = np.array(icon, dtype=np.uint8)
    rgb = arr[:, :, :3].astype(np.float32)
    lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]

    white = lum > 185
    ys, xs = np.where(white)
    if len(xs) == 0:
        return icon

    inside = np.zeros(lum.shape, dtype=bool)
    inside[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1] = True
    crown = inside & (lum < 140)

    out = arr.copy()
    out[crown, 0] = crown_purple[0]
    out[crown, 1] = crown_purple[1]
    out[crown, 2] = crown_purple[2]
    return Image.fromarray(out, "RGBA")


def main():
    track_out = os.path.join(
        MOD, "gfx", "interface", "illustrations", "legacy_tracks", "penumbra_legacy_track.dds"
    )
    icon_out = os.path.join(MOD, "gfx", "interface", "icons", "dynasty", "penumbra_legacy_track.dds")
    os.makedirs(os.path.dirname(track_out), exist_ok=True)
    os.makedirs(os.path.dirname(icon_out), exist_ok=True)

    track = compose_track()
    icon = make_dynasty_icon()
    track.save(track_out)
    icon.save(icon_out)

    track_mean = ImageStat.Stat(track.convert("RGB")).mean
    icon_mean = ImageStat.Stat(icon.convert("RGB")).mean
    print(f"track: {track_out} {track.size} mean={track_mean}")
    print(f"icon:  {icon_out} {icon.size} mean={icon_mean}")


if __name__ == "__main__":
    main()