from pathlib import Path

BOM = b"\xef\xbb\xbf"
ROOT = (Path(__file__).resolve().parents[1] / "lasombra_court")
loc = ROOT / "localization" / "english" / "lasombra_court_l_english.yml"
raw = loc.read_bytes()
text = raw[3:].decode("utf-8") if raw.startswith(BOM) else raw.decode("utf-8")
block = """
 # Reclothe court decision (v1.40.63)
 lasombra_court_reclothe_court_decision: "Reclothe the Court"
 lasombra_court_reclothe_court_decision_desc: "Strip lingering revel flags so characters wear clothes again on the map and in court.\\n\\n#weak Clears #V is_naked#!, salon nude, PoD force-nudity, and activity cloak/revel flags on you, your courtiers, guests, and any leftover orgy portrait targets. Safe to use after an Umbral Orgy or Court of Shadows activity that left someone undressed.#!"
 lasombra_court_reclothe_court_decision_confirm: "Dress them."
 lasombra_court_reclothe_court_decision_tooltip: "Clear stuck nude/revel portrait flags across your court."
 lasombra_court_reclothe_court_decision_effect_tt: "You, your courtiers, and guests lose stuck revel/nude flags and dress normally again."
 lasombra_court_reclothe_court_toast_title: "Court Reclothed"
 lasombra_court_reclothe_court_toast_desc: "Lingering revel attire and nude flags have been cleared."
"""
if "lasombra_court_reclothe_court_decision:" not in text:
    if not text.endswith("\n"):
        text += "\n"
    text += block.lstrip("\n")
    if not text.endswith("\n"):
        text += "\n"
    loc.write_bytes(BOM + text.encode("utf-8"))
    print("loc appended")
else:
    print("loc already present")

for rel in (
    "common/scripted_effects/17_lasombra_court_portrait_effects.txt",
    "common/scripted_triggers/09_lasombra_court_portrait_triggers.txt",
    "common/scripted_effects/09_lasombra_court_activity_effects.txt",
    "common/scripted_effects/02_lasombra_court_umbral_orgy_summary_effects.txt",
    "common/scripted_effects/11_lasombra_court_umbral_orgy_chain_effects.txt",
    "common/on_action/zz_lasombra_court_yearly_pulse.txt",
    "common/decisions/00_lasombra_court_decisions.txt",
    "common/activities/activity_types/zz_lasombra_court_black_chapel_procession.txt",
    "common/activities/activity_types/zz_lasombra_court_veiled_pursuit.txt",
    "events/02_lasombra_court_umbral_orgy_events.txt",
):
    p = ROOT / rel
    raw = p.read_bytes()
    if not raw.startswith(BOM):
        p.write_bytes(BOM + raw)
        print("bom", rel)
    else:
        print("ok", rel)
