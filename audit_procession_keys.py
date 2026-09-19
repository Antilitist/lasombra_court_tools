import os
import re

MOD = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lasombra_court"))
LOC_DIR = os.path.join(MOD, "localization", "english")

loc_keys = set()
for root, dirs, files in os.walk(LOC_DIR):
    for f in files:
        if not f.endswith(".yml"):
            continue
        text = open(os.path.join(root, f), encoding="utf-8-sig").read()
        for m in re.finditer(r"^\s([A-Za-z0-9_.]+):", text, re.M):
            loc_keys.add(m.group(1))

# Files that define procession activity UI
files_to_scan = [
    "common/activities/activity_types/zz_lasombra_court_black_chapel_procession.txt",
    "common/activities/pulse_actions/zz_lasombra_court_procession_pulses.txt",

    "common/activities/guest_invite_rules/zz_lasombra_court_activity_invite_rules.txt",
    "common/activities/activity_group_types/01_lasombra_court_activity_group_types.txt",
    "common/important_actions/zz_lasombra_court_activity_actions.txt",
    "common/scripted_effects/09_lasombra_court_activity_effects.txt",
    "common/scripted_modifiers/zz_lasombra_court_activity_scripted_modifiers.txt",
    "events/11_lasombra_court_procession_events.txt",
]

# Patterns that resolve to localization keys in activity UI
patterns = [
    r"desc\s*=\s*([a-z][a-z0-9_.]+)",
    r"title\s*=\s*([a-z][a-z0-9_.]+)",
    r"name\s*=\s*([a-z][a-z0-9_.]+)",
    r"key\s*=\s*([a-z][a-z0-9_.]+)",
    r"activity_group_type\s*=\s*([a-z][a-z0-9_.]+)",
    r"intents\s*=\s*\{[^}]*\b([a-z][a-z0-9_]+_intent)\b",
]

atype = "activity_lasombra_court_black_chapel_procession"
# CK3 auto-resolved activity keys
auto_keys = [
    atype,
    atype + "_name",
    atype + "_host_an_a",
    atype + "_destination_selection",
    atype + "_desc",
    atype + "_owner",
    atype + "_host_desc",
    atype + "_guest_help_text",
    atype + "_conclusion_desc",
    atype + "_selection_tooltip",
    "TRAVEL_NAME_FOR_" + atype,
]

missing = []
found_refs = []

for rel in files_to_scan:
    path = os.path.join(MOD, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        continue
    content = open(path, encoding="utf-8").read()
    for i, line in enumerate(content.splitlines(), 1):
        for pat in patterns:
            for m in re.finditer(pat, line):
                k = m.group(1)
                if k.startswith(("activity_", "lasombra_court_", "action_can_host_lasombra", "reduce_stress", "befriend")) or "procession" in k or "seduce" in k or "rite_scale" in k or "invite" in k:
                    found_refs.append((k, rel, i))
                    if k not in loc_keys:
                        missing.append((k, rel, i))

for k in auto_keys:
    found_refs.append((k, "CK3_convention", 0))
    if k not in loc_keys:
        missing.append((k, "CK3_convention", 0))

# pulse actions need display name + log + log_title
pulse_file = os.path.join(MOD, "common/activities/pulse_actions/zz_lasombra_court_procession_pulses.txt")
for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", open(pulse_file, encoding="utf-8").read(), re.M):
    pa = m.group(1)
    for suffix in ("", "_log", "_log_title"):
        k = pa + suffix
        found_refs.append((k, pulse_file, 0))
        if k not in loc_keys:
            missing.append((k, "pulse_action_pattern", 0))

# option blocks in activity file
act_content = open(os.path.join(MOD, "common/activities/activity_types/zz_lasombra_court_black_chapel_procession.txt"), encoding="utf-8").read()
for m in re.finditer(r"\b(lasombra_court_[a-z0-9_]+)\s*=\s*\{", act_content):
    k = m.group(1)
    for suffix in ("", "_desc"):
        kk = k + suffix
        if kk not in loc_keys and ("procession" in kk or "rite" in kk or "vigil" in kk):
            missing.append((kk, "option_or_phase_pattern", 0))

print("=== PROCESSION KEYS MISSING FROM LOC ===")
for item in sorted(set(missing), key=lambda x: x[0]):
    print(f"{item[0]}  <-  {item[1]}:{item[2]}")

print(f"\nTotal missing: {len(set(missing))}")
print(f"Total refs checked: {len(found_refs)}")

# where are activity keys defined?
print("\n=== WHERE ACTIVITY KEYS LIVE ===")
for k in sorted(auto_keys):
    if k in loc_keys:
        for root, dirs, files in os.walk(LOC_DIR):
            for f in files:
                if not f.endswith(".yml"):
                    continue
                p = os.path.join(root, f)
                if re.search(rf"^\s{k}:", open(p, encoding="utf-8-sig").read(), re.M):
                    print(f"  {k} -> {os.path.relpath(p, LOC_DIR)}")