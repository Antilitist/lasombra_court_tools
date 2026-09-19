# Cleanup pass v1.40.62 — UTF-8 BOM on CoS scripts + append missing loc keys.
from pathlib import Path

ROOT = (Path(__file__).resolve().parents[1] / "lasombra_court")
BOM = b"\xef\xbb\xbf"

TEXT_EXTS = {".txt", ".yml", ".gui", ".info", ".md"}
SKIP_DIRS = {"tools", ".git", "__pycache__", "backup_umbral_orgy_pre_staged_v1_25", "disabled_gui", "texconv"}


def ensure_bom(path: Path) -> bool:
    raw = path.read_bytes()
    if raw.startswith(BOM):
        return False
    # strip any existing UTF-16 etc. — assume utf-8/latin-1-ish
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
    path.write_bytes(BOM + text.encode("utf-8"))
    return True


def main():
    bom_fixed = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_EXTS:
            continue
        # Only game data trees
        rel = p.relative_to(ROOT).as_posix()
        if not (
            rel.startswith("common/")
            or rel.startswith("events/")
            or rel.startswith("gui/")
            or rel.startswith("localization/")
            or rel.startswith("gfx/")
            or rel.startswith("music/")
            or rel.startswith("history/")
            or rel.startswith("data_binding/")
            or p.name == "descriptor.mod"
        ):
            continue
        if ensure_bom(p):
            bom_fixed.append(rel)

    loc = ROOT / "localization" / "english" / "lasombra_court_l_english.yml"
    raw = loc.read_bytes()
    text = raw[3:].decode("utf-8") if raw.startswith(BOM) else raw.decode("utf-8")

    append_bits = []
    keys = {
        "lasombra_court_embrace_petition_memory:": ' lasombra_court_embrace_petition_memory: "Asked for the Embrace"',
        "lasombra_court_received_embrace_petition_memory:": ' lasombra_court_received_embrace_petition_memory: "Received an Embrace petition"',
        "lasombra_court_embrace_petition_granted_memory:": ' lasombra_court_embrace_petition_granted_memory: "Embrace petition granted"',
        "lasombra_court_embrace_petition_performed_memory:": ' lasombra_court_embrace_petition_performed_memory: "Granted an Embrace petition"',
        "lasombra_court_umbral_crossing_desc_general:": ' lasombra_court_umbral_crossing_desc_general: "Prepare the Black Chapel for the Umbral Crossing — Heaven before the Night, then blood."',
    }
    for key, line in keys.items():
        if key not in text:
            append_bits.append(line)

    # Soft-dedupe: remove CoS redefinition of PoD trait_lasombra if both keys exist in our file only once is fine;
    # trait_lasombra conflict is CoS vs PoD — leave CoS keys (load order last wins).

    if append_bits:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n # Cleanup pass v1.40.62 — memory names + scheme desc_general\n"
        text += "\n".join(append_bits) + "\n"
        loc.write_bytes(BOM + text.encode("utf-8"))
        print("loc appended", len(append_bits))
    else:
        print("loc keys already present")

    # Crossing yml file also get scheme alias if separate
    crossing = ROOT / "localization" / "english" / "lasombra_court_crossing_l_english.yml"
    if crossing.exists():
        craw = crossing.read_bytes()
        ctext = craw[3:].decode("utf-8") if craw.startswith(BOM) else craw.decode("utf-8")
        if "lasombra_court_umbral_crossing_desc_general:" not in ctext:
            if not ctext.endswith("\n"):
                ctext += "\n"
            ctext += ' lasombra_court_umbral_crossing_desc_general: "Prepare the Black Chapel for the Umbral Crossing — Heaven before the Night, then blood."\n'
            if "lasombra_court_umbral_crossing_scheme_desc:" in ctext and "lasombra_court_umbral_crossing_desc_general:" in ctext:
                pass
            crossing.write_bytes(BOM + ctext.encode("utf-8"))
            print("crossing loc updated")
        if not craw.startswith(BOM):
            ensure_bom(crossing)

    print("BOM fixed files:", len(bom_fixed))
    for r in bom_fixed[:40]:
        print(" ", r)
    if len(bom_fixed) > 40:
        print(f"  ... +{len(bom_fixed)-40} more")


if __name__ == "__main__":
    main()
