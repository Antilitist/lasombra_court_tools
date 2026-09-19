import os
import re

MOD = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lasombra_court"))
LOC_DIR = os.path.join(MOD, "localization", "english")

loc_keys = {}
for root, dirs, files in os.walk(LOC_DIR):
    for f in files:
        if not f.endswith(".yml"):
            continue
        rel = os.path.relpath(os.path.join(root, f), LOC_DIR)
        text = open(os.path.join(root, f), encoding="utf-8-sig").read()
        for i, line in enumerate(text.splitlines(), 1):
            m = re.match(r"^\s([A-Za-z0-9_.]+):", line)
            if m:
                loc_keys[m.group(1)] = rel

SKIP = {
    "yes", "no", "root", "scope", "value", "add", "limit", "modifier", "character",
    "target", "faith", "via_tenebrarum", "lasombra", "lasombra_court", "revenant",
    "lustful", "zealous", "chaste", "grateful_opinion", "incapable", "adult",
}

# Collect defined game object IDs that need loc
needs_loc = []

def walk_txt(base):
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.endswith(".txt"):
                yield os.path.join(root, f)

# Traits
for p in walk_txt(os.path.join(MOD, "common", "traits")):
    for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", open(p, encoding="utf-8").read(), re.M):
        k = m.group(1)
        if "lasombra" in k:
            for sfx in ("trait_" + k, "trait_" + k + "_desc", "trait_" + k + "_character_desc"):
                needs_loc.append((sfx, p, "trait"))

# Modifiers
for p in walk_txt(os.path.join(MOD, "common", "modifiers")):
    for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", open(p, encoding="utf-8").read(), re.M):
        k = m.group(1)
        if "lasombra" in k:
            needs_loc.append((k, p, "modifier"))
            needs_loc.append((k + "_desc", p, "modifier_desc"))

# Buildings
for p in walk_txt(os.path.join(MOD, "common", "buildings")):
    content = open(p, encoding="utf-8").read()
    for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", content, re.M):
        k = m.group(1)
        if "lasombra" in k:
            needs_loc.append((k, p, "building"))
            needs_loc.append((k + "_desc", p, "building_desc"))
    for m in re.finditer(r"^(building_type_[a-z0-9_]+)\s*=\s*\{", content, re.M):
        k = m.group(1)
        needs_loc.append((k, p, "building_type"))
        needs_loc.append((k + "_desc", p, "building_type_desc"))

# Court positions
for p in walk_txt(os.path.join(MOD, "common", "court_positions")):
    content = open(p, encoding="utf-8").read()
    for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", content, re.M):
        k = m.group(1)
        if "lasombra" in k:
            if "task" in k:
                needs_loc.append((k, p, "cp_task"))
                needs_loc.append((k + "_desc", p, "cp_task_desc"))
            elif "court_position" in k:
                needs_loc.append((k, p, "court_position"))
                needs_loc.append((k + "_desc", p, "court_position_desc"))
                needs_loc.append((k + "_employer_custom_effect_description", p, "cp_employer"))

# Decisions
for p in walk_txt(os.path.join(MOD, "common", "decisions")):
    for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", open(p, encoding="utf-8").read(), re.M):
        k = m.group(1)
        if "lasombra" in k:
            for sfx in ("", "_desc", "_confirm", "_tooltip", "_effect_tt"):
                needs_loc.append((k + sfx, p, "decision"))

# Interactions
for p in walk_txt(os.path.join(MOD, "common", "character_interactions")):
    for m in re.finditer(r"^([a-z][a-z0-9_]+)\s*=\s*\{", open(p, encoding="utf-8").read(), re.M):
        k = m.group(1)
        if "lasombra" in k:
            needs_loc.append((k, p, "interaction"))
            needs_loc.append((k + "_desc", p, "interaction_desc"))

# Music
for p in walk_txt(os.path.join(MOD, "music")):
    content = open(p, encoding="utf-8").read()
    for m in re.finditer(r"music\s*=\s*([a-z][a-z0-9_]+)", content):
        needs_loc.append((m.group(1), p, "music"))
    for m in re.finditer(r"name\s*=\s*\"?([a-z][a-z0-9_]+)\"?", content):
        k = m.group(1)
        if "lasombra" in k:
            needs_loc.append((k, p, "music_cat"))

# desc=/title=/key= assignments
for p in walk_txt(MOD):
    if "localization" in p.replace("\\", "/"):
        continue
    if not p.endswith((".txt", ".gui")):
        continue
    rel = os.path.relpath(p, MOD)
    for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
        for m in re.finditer(r"(?:desc|title|text|name|key|global|first|third)\s*=\s*([a-z][a-z0-9_.]+)", line):
            k = m.group(1)
            if k in SKIP or "." in k and not k.startswith("lasombra_court."):
                continue
            if "lasombra" in k or k.startswith("activity_lasombra") or k.startswith("action_lasombra") or k.startswith("action_can_host_lasombra"):
                needs_loc.append((k, rel, i))

missing = []
for k, src, kind in needs_loc:
    if k not in loc_keys:
        missing.append((k, src, kind))

# dedupe
seen = set()
out = []
for item in sorted(missing, key=lambda x: (x[0], str(x[1]))):
    if item[0] in seen:
        continue
    seen.add(item[0])
    src = os.path.relpath(item[1], MOD) if isinstance(item[1], str) and os.path.isfile(item[1]) else item[1]
    out.append((item[0], src, item[2]))

print("=== ALL MISSING LOCALIZATION KEYS ===")
for k, src, kind in out:
    print(f"{k}  [{kind}]  <- {src}")

print(f"\nTotal unique missing: {len(out)}")