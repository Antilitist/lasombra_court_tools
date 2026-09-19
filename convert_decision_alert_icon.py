"""Build per-decision Court of Shadows notification icons (432x144, 3 alert states).

Each icon composites the decision's action illustration inside the vanilla diamond
bezel, matching the art shown on the decision card.
"""
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import math
import os

MOD = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lasombra_court"))
CK3 = r"D:\Games\steamapps\common\Crusader Kings III\game"

VANILLA_ALERT = os.path.join(
    CK3, "gfx", "interface", "icons", "alerts", "action_take_decision.dds"
)
ALERT_DIR = os.path.join(MOD, "gfx", "interface", "icons", "alerts")
PREVIEW_DIR = os.path.join(MOD, "tools")

SIZE = 144
CX = CY = SIZE // 2
INNER_RADIUS = 55
STATE_BRIGHTNESS = (1.0, 1.14, 0.8)

DECISION_ALERTS = {
    "action_lasombra_court_embrace_decision": os.path.join(
        MOD, "gfx/interface/illustrations/decisions/lasombra_court_embrace_decision.dds"
    ),
    "action_lasombra_court_adopt_faith_decision": os.path.join(
        MOD, "gfx/interface/illustrations/decisions/lasombra_court_adopt_faith_decision.dds"
    ),
    "action_lasombra_court_adopt_culture_decision": os.path.join(
        MOD, "gfx/interface/illustrations/decisions/lasombra_court_adopt_culture_decision.dds"
    ),
    "action_lasombra_court_create_head_of_faith_decision": os.path.join(
        CK3, "gfx/interface/illustrations/decisions/decision_personal_religious.dds"
    ),
    "action_lasombra_court_search_umbral_consorts_decision": os.path.join(
        MOD, "gfx/interface/illustrations/decisions/lasombra_court_umbral_consort_decision.dds"
    ),
    "action_lasombra_court_umbral_orgy_decision": os.path.join(
        MOD, "gfx/interface/illustrations/decisions/lasombra_court_umbral_orgy_decision.dds"
    ),
    "action_lasombra_court_umbral_lust_decision": os.path.join(
        MOD, "gfx/interface/illustrations/decisions/lasombra_court_umbral_lust_decision.dds"
    ),
}


def diamond_points(cx, cy, radius):
    return [(cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)]


def point_in_poly(x, y, poly):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        intersect = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi
        )
        if intersect:
            inside = not inside
        j = i
    return inside


def crop_square_cover(img, side):
    w, h = img.size
    if w >= h:
        left = (w - h) // 2
        img = img.crop((left, 0, left + h, h))
    else:
        top = (h - w) // 2
        img = img.crop((0, top, w, top + w))
    return img.resize((side, side), Image.LANCZOS)


def prepare_art(path, brightness):
    img = Image.open(path).convert("RGBA")
    art = crop_square_cover(img, INNER_RADIUS * 2 - 6)
    rgb = ImageEnhance.Contrast(art.convert("RGB")).enhance(1.06)
    rgb = ImageEnhance.Color(rgb).enhance(1.08)
    art = rgb.convert("RGBA")
    if brightness != 1.0:
        bands = art.split()
        gray = ImageEnhance.Brightness(Image.merge("RGBA", bands)).enhance(brightness)
        art = gray
    return art.filter(ImageFilter.UnsharpMask(radius=1.0, percent=80, threshold=2))


def draw_art_fill(art, brightness):
    inner = diamond_points(CX, CY, INNER_RADIUS)
    fill = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    px = fill.load()
    ox = CX - art.width // 2
    oy = CY - art.height // 2
    art_px = art.load()
    for y in range(SIZE):
        for x in range(SIZE):
            if not point_in_poly(x, y, inner):
                continue
            ax, ay = x - ox, y - oy
            if 0 <= ax < art.width and 0 <= ay < art.height:
                r, g, b, a = art_px[ax, ay]
                if a < 8:
                    px[x, y] = (12, 6, 18, 255)
                else:
                    px[x, y] = (r, g, b, 255)
            else:
                px[x, y] = (12, 6, 18, 255)
    return fill


def extract_bezel(frame):
    bezel = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    out = bezel.load()
    src = frame.load()
    inner = diamond_points(CX, CY, INNER_RADIUS)
    for y in range(SIZE):
        for x in range(SIZE):
            r, g, b, a = src[x, y]
            if a < 20:
                continue
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            if lum <= 48 or not point_in_poly(x, y, inner):
                out[x, y] = (r, g, b, a)
    return bezel


def compose_frame(frame, art_path, brightness):
    art = prepare_art(art_path, brightness)
    sigil = draw_art_fill(art, brightness)
    composed = Image.alpha_composite(sigil, extract_bezel(frame))
    mask = frame.split()[3]
    final = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    final.paste(composed, (0, 0), mask)
    return final


def build_alert_icon(icon_name, art_path):
    vanilla = Image.open(VANILLA_ALERT).convert("RGBA")
    sheet = Image.new("RGBA", (SIZE * 3, SIZE), (0, 0, 0, 0))
    for i, bright in enumerate(STATE_BRIGHTNESS):
        frame = vanilla.crop((i * SIZE, 0, (i + 1) * SIZE, SIZE))
        sheet.paste(compose_frame(frame, art_path, bright), (i * SIZE, 0))
    out = os.path.join(ALERT_DIR, f"{icon_name}.dds")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sheet.save(out)
    preview = os.path.join(PREVIEW_DIR, f"preview_{icon_name}.png")
    sheet.save(preview)
    print(f"wrote {out} from {art_path}")


def main():
    for icon_name, art_path in DECISION_ALERTS.items():
        if not os.path.isfile(art_path):
            raise FileNotFoundError(art_path)
        build_alert_icon(icon_name, art_path)


if __name__ == "__main__":
    main()