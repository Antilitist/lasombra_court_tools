"""Audit Court of Shadows activity files for missing English localization keys."""
import os
import re

MOD = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lasombra_court"))
LOC_DIR = os.path.join(MOD, "localization", "english")

loc_keys = set()
for root, _dirs, files in os.walk(LOC_DIR):
    for f in files:
        if not f.endswith(".yml"):
            continue
        text = open(os.path.join(root, f), encoding="utf-8-sig").read()
        for m in re.finditer(r"^\s([A-Za-z0-9_.]+):", text, re.M):
            loc_keys.add(m.group(1))

# Vanilla keys we expect from base game / EP2 (do not flag as missing)
# Scripted effects/triggers/backgrounds — not player-facing localization
SCRIPTED_OK = {
    "lasombra_court_activity_apply_revel_attire_effect",
    "lasombra_court_activity_attempt_conversion_effect",
    "lasombra_court_activity_attendee_pair_trigger",
    "lasombra_court_activity_attendee_partner_trigger",
    "lasombra_court_activity_clear_cult_pair_flags_effect",
    "lasombra_court_activity_clear_revel_attire_effect",
    "lasombra_court_activity_complete_seduce_intent_effect",
    "lasombra_court_activity_conclusion",
    "lasombra_court_activity_guest_trigger",
    "lasombra_court_activity_host_can_start_trigger",
    "lasombra_court_activity_host_shown_trigger",
    "lasombra_court_activity_host_sip_resonance_effect",
    "lasombra_court_activity_lustful_ruler_trigger",
    "lasombra_court_activity_pair_attendees_effect",
    "lasombra_court_activity_pontifical_option_valid_trigger",
    "lasombra_court_activity_seduction_become_lovers_effect",
    "lasombra_court_activity_seduction_ensure_mutual_attraction_effect",
    "lasombra_court_activity_seduction_set_lover_effect",
    "lasombra_court_activity_show_conclusion_background_effect",
    "lasombra_court_notifyable_activity_trigger",
    "lasombra_court_procession_conclusion_effect",
    "lasombra_court_procession_pick_story_guest_effect",
    "lasombra_court_procession_seduce_target_effect",
    "lasombra_court_umbral_consort",
    "lasombra_court_umbral_lust_rite",
    "lasombra_court_umbral_orgy",
    "lasombra_court_umbral_orgy_veil_synergy_effect",
    "lasombra_court_veiled_pursuit",
    "lasombra_court_veiled_pursuit_conclusion_effect",
    "lasombra_court_veiled_pursuit_light_pairing_effect",
    "lasombra_court_veiled_pursuit_light_pairing_pass_effect",
}

VANILLA_OK = {
    "lasombra_court_activity_intent_complete_toast",
    "lasombra_court_activity_intent_complete_toast_desc",
    "lasombra_court_activity_seduction_awaken_toast",
    "lasombra_court_activity_seduction_awaken_toast_desc",
    "lasombra_court_seduce_attendee_intent",
    "lasombra_court_seduce_attendee_intent_desc",
    "activity_invite_lasombra_court_seduce_targets",
    "activity_invite_lasombra_court_seduce_targets_desc",
    "activity_intent_complete_toast",
    "intent_woo_success_tt",
    "woo_attendee_intent",
    "woo_attendee_intent_desc",
    "befriend_attendee_intent",
    "befriend_attendee_intent_desc",
    "reduce_stress_intent",
    "reduce_stress_intent_desc",
    "activity_invalidated",
    "POD_drink_herd_pause_warning",
    "lover_wedding_seductive_exchange",
    "default_lover_opinion",
    "lover_lasombra_court_activity_seduction",
    "event_message_title",
    "event_message_text",
}

ACTIVITY_GLOBS = [
    "common/activities",
    "events/11_lasombra_court_procession_events.txt",
    "events/12_lasombra_court_veiled_pursuit_events.txt",
    "events/14_lasombra_court_activity_interactive_events.txt",
    "common/scripted_effects/09_lasombra_court_activity_effects.txt",
    "common/scripted_effects/10_lasombra_court_activity_verdict_effects.txt",
    "common/scripted_modifiers/zz_lasombra_court_activity_scripted_modifiers.txt",
    "common/scripted_triggers/05_lasombra_court_activity_triggers.txt",
    "common/scripted_triggers/06_lasombra_court_activity_verdict_triggers.txt",
    "common/important_actions/zz_lasombra_court_activity_actions.txt",
    "common/event_backgrounds/00_lasombra_court_event_backgrounds.txt",
]

PATTERNS = [
    (r"\btitle\s*=\s*([a-z][a-z0-9_.]+)", "title"),
    (r"\bname\s*=\s*(lasombra_court\.[a-z0-9_.]+)", "option"),
    (r"\bdesc\s*=\s*(lasombra_court\.[a-z0-9_.]+)", "desc"),
    (r"\bkey\s*=\s*([a-z][a-z0-9_.]+)", "log_key"),
    (r"\bcustom_tooltip\s*=\s*([a-z][a-z0-9_.]+)", "tooltip"),
    (r"\btext\s*=\s*([a-z][a-z0-9_.]+)", "trigger_text"),
    (r"^([a-z][a-z0-9_]+)\s*=\s*\{", "pulse_or_block"),
]

ACTIVITY_TYPES = [
    "activity_lasombra_court_black_chapel_procession",
    "activity_lasombra_court_veiled_pursuit",
]

AUTO_SUFFIXES = [
    "",
    "_name",
    "_host_an_a",
    "_destination_selection",
    "_desc",
    "_owner",
    "_host_desc",
    "_guest_help_text",
    "_conclusion_desc",
    "_selection_tooltip",
    "_province_desc",
    "_province_capital_desc",
]

files_to_scan = []
for g in ACTIVITY_GLOBS:
    path = os.path.join(MOD, g.replace("/", os.sep))
    if os.path.isfile(path):
        files_to_scan.append(path)
    elif os.path.isdir(path):
        for root, _d, fs in os.walk(path):
            for fn in fs:
                if fn.endswith(".txt"):
                    files_to_scan.append(os.path.join(root, fn))

missing = {}
refs = []

for path in sorted(set(files_to_scan)):
    rel = os.path.relpath(path, MOD)
    content = open(path, encoding="utf-8").read()
    for pat, kind in PATTERNS:
        for m in re.finditer(pat, content, re.M):
            k = m.group(1)
            if not (
                k.startswith(("lasombra_court", "activity_lasombra", "activity_invite_lasombra", "action_can_host_lasombra"))
                or k.endswith("_intent")
                or "procession" in k
                or "pursuit" in k
                or "rite_scale" in k
                or k.startswith("task_lasombra")
            ):
                continue
            if (
                k in VANILLA_OK
                or k in SCRIPTED_OK
                or k.endswith("_effect")
                or k.endswith("_trigger")
            ):
                continue
            refs.append((k, rel, kind))
            if k not in loc_keys:
                missing.setdefault(k, []).append((rel, kind))

# Activity type conventions
for atype in ACTIVITY_TYPES:
    for suffix in AUTO_SUFFIXES:
        k = atype + suffix if suffix else atype
        refs.append((k, "CK3_convention", "auto"))
        if k not in loc_keys and k not in VANILLA_OK:
            missing.setdefault(k, []).append(("CK3_convention", "auto"))
    k = "TRAVEL_NAME_FOR_" + atype
    refs.append((k, "CK3_convention", "auto"))
    if k not in loc_keys:
        missing.setdefault(k, []).append(("CK3_convention", "auto"))

# Pulse / phase / option blocks from activity type files
for atype_file in [
    "common/activities/activity_types/zz_lasombra_court_black_chapel_procession.txt",
    "common/activities/activity_types/zz_lasombra_court_veiled_pursuit.txt",
    "common/activities/pulse_actions/zz_lasombra_court_procession_pulses.txt",
    "common/activities/pulse_actions/zz_lasombra_court_veiled_pursuit_pulses.txt",
]:
    path = os.path.join(MOD, atype_file)
    if not os.path.isfile(path):
        continue
    for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", open(path, encoding="utf-8").read(), re.M):
        base = m.group(1)
        if not base.startswith("lasombra_court"):
            continue
        for suffix in ("", "_desc", "_log", "_log_title"):
            k = base + suffix
            refs.append((k, atype_file, "pattern"))
            if k not in loc_keys and k not in VANILLA_OK:
                missing.setdefault(k, []).append((atype_file, "pattern"))

# Modifiers applied during activities
for mod in [
    "lasombra_court_chapel_consecrated_recently_modifier",
    "lasombra_court_chapel_prepared_modifier",
    "lasombra_court_recent_veiled_pursuit_modifier",
    "lasombra_court_veil_still_warm_modifier",
]:
    refs.append((mod, "modifier", "modifier"))
    if mod not in loc_keys:
        missing.setdefault(mod, []).append(("modifier", "modifier"))

# Guest accept modifier desc keys
for k in [
    "lasombra_court_lustful_ruler_accept",
    "lasombra_court_via_tenebrarum_guest_accept",
    "lasombra_court_lasombra_guest_accept",
    "lasombra_court_chaste_guest_decline",
    "lasombra_court_zealous_guest_decline",
]:
    refs.append((k, "guest_modifier", "desc"))
    if k not in loc_keys:
        missing.setdefault(k, []).append(("guest_modifier", "desc"))

# Event backgrounds
bg_file = os.path.join(MOD, "common/event_backgrounds/00_lasombra_court_event_backgrounds.txt")
if os.path.isfile(bg_file):
    for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", open(bg_file, encoding="utf-8").read(), re.M):
        k = m.group(1)
        refs.append((k, "event_background", "background"))
        if k not in loc_keys:
            missing.setdefault(k, []).append(("event_background", "background"))

print("=== ACTIVITY LOC GAPS (player-visible) ===")
for k in sorted(missing):
    sources = ", ".join(f"{a}({b})" for a, b in missing[k])
    print(f"{k}\n    <- {sources}")

print(f"\nTotal missing keys: {len(missing)}")
print(f"Total refs scanned: {len(refs)}")