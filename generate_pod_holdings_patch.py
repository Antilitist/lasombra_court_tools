"""Regenerate zz_lasombra_court_holdings.txt from PoD's 00_holdings.txt."""
import re
from pathlib import Path

POD_HOLDINGS = Path(
    r"D:\Games\steamapps\workshop\content\1158310\2216659254\common\holdings\00_holdings.txt"
)
OUT = (Path(__file__).resolve().parents[1] / "lasombra_court") / "common" / "holdings" / "zz_lasombra_court_holdings.txt"

ADDITIONS = {
    "castle_holding": "lasombra_court_iron_nocturne_bastion_01",
    "city_holding": "lasombra_court_penumbra_exchange_01",
    "church_holding": "lasombra_court_basilica_ash_01",
    "temple_citadel_holding": "lasombra_court_basilica_ash_01",
}


def main() -> None:
    content = POD_HOLDINGS.read_text(encoding="utf-8-sig")
    for holding, building in ADDITIONS.items():
        pattern = rf"({holding} = \{{.*?\n\tbuildings = \{{)"
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            raise SystemExit(f"Could not find {holding} in PoD holdings")
        if building in content:
            continue
        insert_pos = match.end()
        injection = f"\n\t\t# Court of Shadows — Umbral holding buildings\n\t\t{building}\n"
        content = content[:insert_pos] + injection + content[insert_pos:]
    header = (
        "# Court of Shadows — PoD holding building registration\n"
        "# Regenerate with tools/generate_pod_holdings_patch.py after PoD updates.\n\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + content, encoding="utf-8-sig")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()