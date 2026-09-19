# One-shot: append P1 Iron Nocturne + missing loc keys.
from pathlib import Path

loc = (Path(__file__).resolve().parents[1] / "lasombra_court") / "localization" / "english" / "lasombra_court_l_english.yml"

append = r"""
 # Iron Nocturne focus events (Phase E v1.40.59)
 lasombra_court.0540.t: "The Watch Thins"
 lasombra_court.0540.desc: "On the walls the torches burn low. Scouts report late. Your iron nocturne - the night that does not sleep - has gaps.\n\nA Lasombra prince who lets the watch thin invites both rivals and the Masquerade to slip."
 lasombra_court.0540.a: "Double the watch. Let dread walk the battlements."
 lasombra_court.0540.b: "Pay for better eyes and sharper steel."
 lasombra_court.0540.c: "Push through it. Stress is a tax of command."

 lasombra_court.0541.t: "Volunteer for the Penumbra Guard"
 lasombra_court.0541.desc: "[iron_guard_candidate.GetTitledFirstName] stands before you - not begging, not quite. They want the penumbra guard: night drills, black steel, a place in Iron Nocturne.\n\nThe court watches how you choose who may stand closest to your shadow."
 lasombra_court.0541.a: "Drill them. Make them a blade of the night."
 lasombra_court.0541.b: "Reject them. Only proven steel earns the guard."
 lasombra_court.0541.c: "Make a spectacle of their ambition."
 lasombra_court.0541.c.tt: "Public spectacle risks the Masquerade."

 lasombra_court.0542.t: "Black Sail"
 lasombra_court.0542.desc: "Word reaches you that [iron_black_sail_target.GetTitledFirstName] has grown careless - or bold. Either way, Iron Nocturne has a name for this: Black Sail. A night strike, a broken will, a lesson that travels farther than any decree.\n\nThe question is not whether the night can take them. It is whether you will."
 lasombra_court.0542.a: "Mark them. Let the black sail rise quietly."
 lasombra_court.0542.b: "Strike hard and visible - fear is a sermon."
 lasombra_court.0542.b.tt: "A visible strike risks Masquerade exposure."
 lasombra_court.0542.c: "Not tonight. Let them wonder."

 lasombra_court.0631.t: "The Penumbra Trial"
 lasombra_court.0631.desc: "Iron Nocturne is not only war. It is a court of blades and silence - and tonight your domain demands a trial.\n\nNot a mortal court. A penumbra trial: who may stand in your shadow, and who must learn to fear it."
 lasombra_court.0631.a: "Harsh terms. Let dread set the rules."
 lasombra_court.0631.b: "Measured justice. Prestige binds better than terror alone."
 lasombra_court.0631.c: "Keep it secret. Intrigue will shape the outcome."
 lasombra_court.0631.c.success: "The secret trial is sealed. No gossip leaves the dark."
 lasombra_court.0631.c.failure: "A whisper slips - the Masquerade frays."
 lasombra_court.0631.c.failure.tt: "Risk of increased Masquerade exposure."

 lasombra_court.0632.t: "Choose the Blade"
 lasombra_court.0632.desc: "The trial needs a champion of the penumbra. [penumbra_trial_knight.GetTitledFirstName] is ready - or claims to be.\n\nHow you raise them will echo through every night that follows."
 lasombra_court.0632.a: "Lead them yourself. Your shadow is the standard."
 lasombra_court.0632.b: "Delegate. Let ambition prove itself."
 lasombra_court.0632.c: "Make an example of a rival while you choose."

 lasombra_court.0633.t: "Under the Black Banner"
 lasombra_court.0633.desc: "The penumbra trial reaches its steel. Drills end. Eyes watch. Either prowess or scheme will decide who leaves the circle standing."
 lasombra_court.0633.desc.harsh: "Under harsh terms, the penumbra trial is a cutting edge - no softness, only the night's judgment."
 lasombra_court.0633.desc.secret: "The secret trial unfolds behind veiled doors. Only those who matter will know who prevailed."
 lasombra_court.0633.a: "Meet them in open contest of arms."
 lasombra_court.0633.a.success: "Steel answers for you. The penumbra remembers strength."
 lasombra_court.0633.a.failure: "You falter - the trial scars prestige, not flesh alone."
 lasombra_court.0633.b: "Win through scheme and shadow."
 lasombra_court.0633.c: "Show mercy. Even iron can temper."

 lasombra_court.0634.t: "Night Holds"
 lasombra_court.0634.desc: "The Penumbra Trial ends. Your court has a new story of the night - and Iron Nocturne has teeth again."
 lasombra_court.0634.desc.mercy: "Mercy is not weakness when spoken from a throne of shadow. The trial ends; loyalty deepens."
 lasombra_court.0634.desc.scheme: "No blade was needed. The scheme did the work. That, too, is Iron Nocturne."
 lasombra_court.0634.a: "Claim the victor's mantle - prestige and a lasting edge."
 lasombra_court.0634.b: "Spend the fear. Let dread do the teaching."

 lasombra_court_iron_night_watch_modifier: "Doubled Night Watch"
 lasombra_court_iron_night_watch_modifier_desc: "Extra eyes on the walls. Prestige and dread from a court that does not sleep lightly."
 lasombra_court_iron_drilled_guard_modifier: "Penumbra Drill"
 lasombra_court_iron_drilled_guard_modifier_desc: "Night drills and black discipline. Knights and prowess answer more cleanly."
 lasombra_court_iron_black_sail_modifier: "Black Sail Marked"
 lasombra_court_iron_black_sail_modifier_desc: "A night-strike doctrine. Hostile schemes and dread gain bite."
 lasombra_court_iron_penumbra_trial_victor_modifier: "Penumbra Trial Victor"
 lasombra_court_iron_penumbra_trial_victor_modifier_desc: "The trial is remembered. Prestige, dread, and another knight's place in the dark."

 lasombra_court_salon_shadow_momentum_active_modifier: "Shadow Momentum"
 lasombra_court_salon_shadow_momentum_active_modifier_desc: "Pursuit and attack advantage from Iron Nocturne doctrine - the night moves first."
 lasombra_court_salon_prince_of_penumbra_modifier: "Prince of the Penumbra"
 lasombra_court_salon_prince_of_penumbra_modifier_desc: "Salon mastery: prestige and a court that bends toward soft shadows."
 lasombra_court_salon_ash_liturgy_modifier: "Ash Liturgy Eternal"
 lasombra_court_salon_ash_liturgy_modifier_desc: "Mastery of ash and absolution: piety and stress relief."
 lasombra_court_salon_iron_nocturne_modifier: "Iron Nocturne"
 lasombra_court_salon_iron_nocturne_modifier_desc: "Mastery of the iron night: prowess, knights, and dread that does not fade."
 lasombra_court_salon_sanguine_court_modifier: "Prince's Table"
 lasombra_court_salon_sanguine_court_modifier_desc: "Sanguine mastery: prestige and a court that feeds loyalty as well as blood."

 lasombra_court_amici_whisper_court_position_employer_custom_effect_description: "$lasombra_court_amici_whisper_employer_custom_effect_description$"
 lasombra_court_blood_arbiter_court_position_employer_custom_effect_description: "$lasombra_court_blood_arbiter_employer_custom_effect_description$"
 lasombra_court_blood_confessor_court_position_employer_custom_effect_description: "$lasombra_court_blood_confessor_employer_custom_effect_description$"
 lasombra_court_eclipse_cupbearer_court_position_employer_custom_effect_description: "$lasombra_court_eclipse_cupbearer_employer_custom_effect_description$"
 lasombra_court_herd_binder_court_position_employer_custom_effect_description: "$lasombra_court_herd_binder_employer_custom_effect_description$"
 lasombra_court_saturnalia_master_court_position_employer_custom_effect_description: "$lasombra_court_saturnalia_master_employer_custom_effect_description$"
 lasombra_court_shadow_harem_keeper_court_position_employer_custom_effect_description: "$lasombra_court_shadow_harem_keeper_employer_custom_effect_description$"
 lasombra_court_thrall_master_court_position_employer_custom_effect_description: "$lasombra_court_thrall_master_employer_custom_effect_description$"

 lasombra_court_spawn_umbral_council_test_courtiers_decision_effect_tt: "Spawns five debug courtiers engineered for every Umbral Council seat."
 lasombra_court_veil_council_legacy_save_decision_confirm: "I understand."
 lasombra_court_veil_council_legacy_save_decision_effect_tt: "Explains why new council seats may be empty on a pre-update save."

 lasombra_court_chancellor_shadow_pact_bound_modifier_desc: "A vassal bound by shadow pact - quieter schemes, firmer loyalty."
 lasombra_court_seneschal_night_tithe_county_modifier_desc: "Night tithe drawn from this county's shadowed wealth."
 lasombra_court_chancellor_shadow_pact_no_valid_vassal: "No valid vassal for a Shadow Pact"
 lasombra_court_legate_preach_no_valid_county: "No valid county for the Legate to preach"
 lasombra_court_night_watch_no_valid_county: "No valid county for the Night Watch"
 lasombra_court_seneschal_night_tithe_no_valid_county: "No valid county for the Night Tithe"

 trait_lasombra: "Lasombra"
 trait_lasombra_desc: "Of the clan of shadows - mirrors fail them, but ambition does not."
 trait_lasombra_character_desc: "This character carries Lasombra blood - the Abyss in the veins."
"""

raw = loc.read_bytes()
if raw.startswith(b"\xef\xbb\xbf"):
    text = raw[3:].decode("utf-8")
else:
    text = raw.decode("utf-8")

# Avoid double-append on re-run
if "lasombra_court.0540.t:" in text:
    print("already present; skip")
else:
    if not text.endswith("\n"):
        text += "\n"
    text += append.lstrip("\n")
    if not text.endswith("\n"):
        text += "\n"
    loc.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
    print("appended", loc.stat().st_size)

text = loc.read_text(encoding="utf-8-sig")
for k in (
    "lasombra_court.0540.t:",
    "lasombra_court.0634.b:",
    "trait_lasombra:",
    "lasombra_court_salon_iron_nocturne_modifier:",
):
    print(k, "OK" if k in text else "MISSING")
