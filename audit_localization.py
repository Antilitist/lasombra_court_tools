import os
import re
from collections import defaultdict

MOD = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lasombra_court"))
LOC_DIR = os.path.join(MOD, "localization", "english")

loc_keys = {}
loc_files = []
yaml_risks = []
duplicates = defaultdict(list)

for root, dirs, files in os.walk(LOC_DIR):
    for f in sorted(files):
        if not f.endswith(".yml"):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, LOC_DIR)
        loc_files.append(rel)
        raw = open(path, "rb").read()
        text = raw.decode("utf-8-sig")
        lines = text.splitlines()

        if not raw.startswith(b"\xef\xbb\xbf"):
            yaml_risks.append((rel, 1, "MISSING_UTF8_BOM", "File lacks UTF-8 BOM"))

        if lines and lines[0].strip() != "l_english:":
            yaml_risks.append((rel, 1, "BAD_HEADER", repr(lines[0])))

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            m = re.match(r"^(\s*)([A-Za-z0-9_.]+):\s*(.*)$", line)
            if not m:
                if "\t" in line:
                    yaml_risks.append((rel, i, "TAB_INDENT", line[:80]))
                continue
            indent, key, val = m.group(1), m.group(2), m.group(3)
            if len(indent) != 1 and key != "l_english":
                yaml_risks.append((rel, i, "INDENT_NOT_1_SPACE", f"indent={len(indent)} key={key}"))

            duplicates[key].append((rel, i))
            loc_keys[key] = (rel, i)

            if val and not val.startswith('"') and not val.startswith("'") and val != "0":
                if ":" in val and not val.startswith("#"):
                    yaml_risks.append((rel, i, "UNQUOTED_COLON", f"{key}: {val[:60]}"))
            if val.count('"') % 2 == 1:
                yaml_risks.append((rel, i, "ODD_DOUBLE_QUOTES", key))

GAME_DIRS = ["common", "events", "gui", "music", "data_binding"]
REF_PATTERNS = [
    (r"(?:desc|title|text|name|key)\s*=\s*([a-z][a-z0-9_]+)", "assignment"),
    (r"localization_key\s*=\s*([a-z][a-z0-9_]+)", "custom_loc"),
    (r"important_action_type\s*=\s*([a-z][a-z0-9_]+)", "action"),
    (r"icon\s*=\s*(action_[a-z][a-z0-9_]+)", "action_icon"),
]

refs = defaultdict(list)

for gdir in GAME_DIRS:
    gpath = os.path.join(MOD, gdir)
    if not os.path.isdir(gpath):
        continue
    for root, dirs, files in os.walk(gpath):
        for f in files:
            if not f.endswith((".txt", ".gui")):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, MOD)
            for i, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
                for pat, kind in REF_PATTERNS:
                    for m in re.finditer(pat, line):
                        refs[m.group(1)].append((rel, i, kind))

ACTIVITY_TYPES = []
for root, dirs, files in os.walk(os.path.join(MOD, "common", "activities", "activity_types")):
    for f in files:
        if not f.endswith(".txt"):
            continue
        path = os.path.join(root, f)
        content = open(path, encoding="utf-8").read()
        m = re.search(r"^([a-z][a-z0-9_]+)\s*=\s*\{", content, re.M)
        if m:
            ACTIVITY_TYPES.append((m.group(1), os.path.relpath(path, MOD)))

for root, dirs, files in os.walk(os.path.join(MOD, "common", "activities")):
    for f in files:
        if not f.endswith(".txt"):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, MOD)
        content = open(path, encoding="utf-8").read()
        for m in re.finditer(r"\b([a-z][a-z0-9_]+)\s*=\s*\{", content):
            k = m.group(1)
            if k.startswith(("lasombra_court_", "activity_")):
                refs[k].append((rel, 0, "block_id"))

pulse_actions = []
for root, dirs, files in os.walk(os.path.join(MOD, "common", "activities", "pulse_actions")):
    for f in files:
        path = os.path.join(root, f)
        rel = os.path.relpath(path, MOD)
        content = open(path, encoding="utf-8").read()
        for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", content, re.M):
            pulse_actions.append((m.group(1), rel))
        for m in re.finditer(r"key\s*=\s*([a-z][a-z0-9_]+)", content):
            refs[m.group(1)].append((rel, 0, "log_key"))

LASOMBRA_PREFIXES = (
    "lasombra", "activity_lasombra", "action_", "task_lasombra", "tenet_lasombra",
    "tradition_lasombra", "building_lasombra", "building_type_lasombra", "penumbra_",
    "via_", "heritage_lasombra", "language_tenebris", "ethos_umbral", "dynn_",
    "NOT_LASOMBRA", "LASOMBRA_COURT", "TRAVEL_NAME_FOR_activity_lasombra",
    "decision_group_type_lasombra", "activity_group_type_lasombra", "activity_invite_lasombra",
    "recipient_secondary_lasombra", "doctrine_parameter_lasombra", "name_list_lasombra",
    "missing_lasombra", "trait_lasombra_court",
)

SKIP_KEYS = {
    "via_tenebrarum", "lasombra", "lasombra_court", "revenant", "lustful",
    "beauty_good_1", "deviant", "zealous", "chaste", "grateful_opinion",
}

def is_mod_loc_key(k):
    if k in SKIP_KEYS:
        return False
    return any(k.startswith(p) or k == p.rstrip("_") for p in LASOMBRA_PREFIXES) or "lasombra" in k

missing = []
for k, locations in sorted(refs.items()):
    if k in loc_keys or not is_mod_loc_key(k):
        continue
    loc = locations[0]
    missing.append((k, loc[0], loc[1], loc[2]))

activity_gaps = []
for atype, fpath in ACTIVITY_TYPES:
    for suffix in ("", "_name", "_desc"):
        r = atype + suffix
        if r not in loc_keys:
            activity_gaps.append((r, fpath, "REQUIRED_ACTIVITY_KEY"))

pulse_gaps = []
for pa, fpath in pulse_actions:
    if pa + "_log" not in loc_keys:
        pulse_gaps.append((pa + "_log", fpath, "missing_log"))
    if pa + "_log_title" not in loc_keys:
        pulse_gaps.append((pa + "_log_title", fpath, "missing_log_title"))
    if pa not in loc_keys:
        pulse_gaps.append((pa, fpath, "missing_pulse_display_name"))

print("=== LOC FILES ===")
for f in loc_files:
    print(f)
print(f"Total loc keys: {len(loc_keys)}")

print("\n=== DUPLICATE KEYS (across files) ===")
for k, locs in sorted(duplicates.items()):
    files = set(x[0] for x in locs)
    if len(files) > 1:
        print(f"{k}: {locs}")

print("\n=== DUPLICATE KEYS (within same file) ===")
for k, locs in sorted(duplicates.items()):
    if len(locs) > 1:
        files = [x[0] for x in locs]
        if len(files) == len(set(files)):
            continue
        print(f"{k}: {locs}")

print("\n=== ACTIVITY PATTERN GAPS ===")
for g in activity_gaps:
    print(f"{g[0]} ({g[2]}) ref in {g[1]}")

print("\n=== PULSE ACTION GAPS ===")
for g in pulse_gaps:
    print(f"{g[0]} ({g[2]}) in {g[1]}")

print("\n=== MISSING LOCALIZATION ===")
for item in missing:
    print(f"{item[0]}: {item[1]}:{item[2]} ({item[3]})")

print("\n=== YAML RISKS ===")
for r in yaml_risks:
    print(f"{r[0]}:{r[1]} [{r[2]}] {r[3]}")
print(f"Total yaml risks: {len(yaml_risks)}")

act_sub = [k for k, v in loc_keys.items() if k.startswith("activity_lasombra") and "activities" in v[0]]
act_main = [k for k, v in loc_keys.items() if k.startswith("activity_lasombra") and "activities" not in v[0]]
print(f"\nactivity_lasombra keys in subfolder: {len(act_sub)}, in main: {len(act_main)}")

print("\n=== selection_tooltip wired in game defs ===")
found = False
for root, dirs, files in os.walk(os.path.join(MOD, "common", "activities")):
    for f in files:
        path = os.path.join(root, f)
        if "selection_tooltip" in open(path, encoding="utf-8").read():
            print(os.path.relpath(path, MOD))
            found = True
if not found:
    print("(none)")