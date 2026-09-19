from pathlib import Path

loc = (Path(__file__).resolve().parents[1] / "lasombra_court") / "localization" / "english" / "lasombra_court_l_english.yml"
block = """
 # Resync ghoul/immortal age interaction (v1.40.61)
 lasombra_court_resync_ghoul_age_interaction: "Resync Immortal Age"
 lasombra_court_resync_ghoul_age_interaction_desc: "#D Debug / maintenance.#! Re-runs the PoD age sync used by #V POD_ghoul_maintenance.500#! (birthday 3/6/10/15/16) and force-sets immortal portrait age to this character's current chronological age.\\n\\n#weak Use when a [ghoul|E] or young immortal still looks like a baby/child after aging.#!"
 lasombra_court_resync_ghoul_age_interaction_send: "Resync age"
 lasombra_court_resync_ghoul_age_interaction_notification: "Age resynced"
 lasombra_court_resync_ghoul_age_requires_immortal_tt: "Target must be immortal (ghouls and most vampires are)"
 lasombra_court_resync_ghoul_age_toast_title: "Immortal Age Resynced"
 lasombra_court_resync_ghoul_age_toast_desc: "Portrait/immortal age set to chronological age for [recipient.GetTitledFirstName]."
"""
raw = loc.read_bytes()
text = raw[3:].decode("utf-8") if raw.startswith(b"\xef\xbb\xbf") else raw.decode("utf-8")
if "lasombra_court_resync_ghoul_age_interaction:" in text:
    print("already present")
else:
    if not text.endswith("\n"):
        text += "\n"
    text += block.lstrip("\n")
    if not text.endswith("\n"):
        text += "\n"
    loc.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
    print("appended")
