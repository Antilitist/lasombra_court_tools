# Salon of Night — Custom Lifestyle Design Draft (v1.40.0 target)

Court of Shadows character progression: **courtcraft, sacrament, war-dread, and appetite** — not PoD disciplines.

---

## Identity

| Field | Value |
|-------|-------|
| **Lifestyle key** | `salon_of_night_lifestyle` |
| **Player-facing name** | Salon of Night |
| **Gate** | Vampire/revenant/ghoul + (Lasombra **or** Umbral culture **or** Via Tenebrarum **or** Penumbra-Born **or** CoSLA Prodigy employed by Umbral court) |
| **XP** | `base_xp_gain = 8`, `xp_per_level = 1000` |
| **Trees** | 4 (one per focus), 7 perks each (6 + finisher) |

**Does not replace:** PoD discipline lifestyles, vanilla lifestyles, Penumbra Legacy (dynasty passive).

---

## Art direction

### Palette & mood
- Base: `#14141E` ink, `#C9A227` candle-gold accents, `#8B1A1A` blood highlights
- No mirrors, no daylight; candle smoke, black stone, silk veils, black sails

### Asset map (ship v1.40 with placeholders)

| Asset | Path (target) | Source / method |
|-------|----------------|-----------------|
| Lifestyle banner | `gfx/interface/icons/lifestyles/salon_of_night_lifestyle.dds` | Crop `tools/activity_scene_sources/lasombra_court_procession_pulse_blood.jpg` → 220×180; darken 40% |
| Lifestyle tree BG tint | reuse vanilla `lifestyles_tree_area_bg.dds` | GUI: purple progress bar `#4A3B6B` |
| Focus: Salon | `gfx/interface/icons/focus/salon_whispers_focus.dds` | Resize `lasombra_tenet_shadow_harem.dds` |
| Focus: Ash Liturgy | `gfx/interface/icons/focus/ash_liturgy_focus.dds` | Resize `lasombra_tenet_ash_liturgy.dds` |
| Focus: Iron Nocturne | `gfx/interface/icons/focus/iron_nocturne_focus.dds` | Resize `lasombra_tenet_iron_nocturne.dds` |
| Focus: Sanguine Court | `gfx/interface/icons/focus/sanguine_court_focus.dds` | Resize `lasombra_tenet_blood_flock.dds` |
| Node icons (×4 trees) | reuse vanilla `node_intrigue`, `node_learning`, `node_martial`, `node_stewardship` | Per tree |
| Finisher icons (×4) | `gfx/interface/icons/lifestyles_perks/salon_prince_of_penumbra.dds` etc. | Tenet icons @ 64px + gold rim in `convert_lifestyle_perk_icons.py` |

### GUI hooks (`window_character_lifestyle.gui`)
- Add `pod_lifestyle_progressbars` sibling block for `salon_of_night_lifestyle` (purple bar)
- Add `pod_lifestyle_unspent_points` node icon (intrigue node or custom)
- Register in `POD_types_for_vanilla_guis_lifestyle.gui` pattern if PoD tab scroll breaks

### Perk tree layout (all four trees share geometry)

```
        [2]  tier 0 — entry
       /   \
    [1]     [3]  tier 1 — fork
      \   /
       [2]  tier 2 — merge
       /   \
    [1]     [3]  tier 3 — fork
      \   /
       [5]  tier 4 — FINISHER (y=5)
```

Coordinates: tier0 `(2,0)`, tier1 `(1,1.25)(3,1.25)`, tier2 `(2,2.5)`, tier3 `(1,3.75)(3,3.75)`, finisher `(2,5)`.

---

## Focuses

| Focus key | Tree key | Skill tint | Monthly focus bonus |
|-----------|----------|------------|---------------------|
| `salon_whispers_focus` | `salon_whispers` | Intrigue | `monthly_salon_of_night_lifestyle_xp_gain_mult = 0.15` when hosting guests |
| `ash_liturgy_focus` | `ash_liturgy` | Learning | `monthly_piety_gain_mult = 0.1` |
| `iron_nocturne_focus` | `iron_nocturne` | Martial | `dread_gain_mult = 0.1` |
| `sanguine_court_focus` | `sanguine_court` | Stewardship | `monthly_prestige_from_herd_mult` or flat `monthly_prestige = 0.1` |

---

## Perk trees (implementation keys)

### Salon of Whispers
1. `salon_veiled_introduction_perk` — entry
2. `salon_consorts_seal_perk` | `salon_guest_welcome_perk`
3. `salon_whisper_between_courts_perk`
4. `salon_salon_favorite_perk` | `salon_pontifical_charm_perk`
5. `salon_prince_of_penumbra_perk` — **finisher** (`icon = salon_prince_of_penumbra`)

### Ash Liturgy
1. `ash_candleless_rite_perk`
2. `ash_blood_absolution_perk` | `ash_offering_of_ash_perk`
3. `ash_liturgists_voice_perk`
4. `ash_chalice_bearer_perk` | `ash_confessors_weight_perk`
5. `ash_liturgy_eternal_perk` — **finisher**

### Iron Nocturne
1. `nocturne_before_dawn_perk`
2. `nocturne_black_sail_perk` | `nocturne_night_assault_perk`
3. `nocturne_penumbra_knight_perk`
4. `nocturne_trophy_chapel_perk` | `nocturne_shadow_momentum_perk`
5. `nocturne_iron_nocturne_perk` — **finisher**

### Sanguine Court
1. `sanguine_vitae_indulgence_perk`
2. `sanguine_thralls_leash_perk` | `sanguine_salon_votary_perk`
3. `sanguine_blood_flock_perk`
4. `sanguine_mothers_shadow_perk` | `sanguine_fetch_by_night_perk`
5. `sanguine_princes_table_perk` — **finisher**

---

## XP sources (on_action hooks — Phase B)

| Event | XP |
|-------|-----|
| Complete Umbral Orgy | +250 |
| Complete Veiled Pursuit | +175 |
| Complete Long Night Procession | +125 |
| Umbral council task proc (monthly pulse) | +25 |
| Successful embrace fetch trial | +150 |
| Night Reaving peasant capture | +75 |
| Umbral baptism hosted | +100 |
| Penumbra-Born on lifestyle pick | +500 one-time |

---

## Modifiers to add (Phase A)

File: `common/modifiers/02_lasombra_court_salon_lifestyle_modifiers.txt`

Character modifiers referenced by perks — keeps tooltips honest.

---

## CoSLA integration

- Prodigies employed at Umbral court: `salon_of_night_lifestyle` valid alongside discipline access
- Auto-focus weight: match job (Curator → Salon, Legate → Ash Liturgy, Warden → Iron Nocturne, Herd Binder → Sanguine)

---

## Implementation phases

| Phase | Deliverable |
|-------|-------------|
| **A** | Lifestyle + 4 focuses + 28 perks + modifiers + loc (this draft) |
| **B** | XP on_actions + court-position perk checks |
| **C** | Art pipeline script + GUI registration |
| **D** | AI weights + Prodigy default focus |

---

## File checklist

```
common/lifestyles/zz_lasombra_court_salon_lifestyle.txt
common/focuses/zz_lasombra_court_salon_focuses.txt
common/lifestyle_perks/zz_lasombra_court_salon_whispers_tree_perks.txt
common/lifestyle_perks/zz_lasombra_court_ash_liturgy_tree_perks.txt
common/lifestyle_perks/zz_lasombra_court_iron_nocturne_tree_perks.txt
common/lifestyle_perks/zz_lasombra_court_sanguine_court_tree_perks.txt
common/modifiers/02_lasombra_court_salon_lifestyle_modifiers.txt
localization/english/lasombra_court_salon_lifestyle_l_english.yml
gfx/interface/icons/lifestyles/salon_of_night_lifestyle.dds
tools/convert_lifestyle_perk_icons.py
```

Localization is **authoritative for player-facing text** — implement perks to match `_effect` strings exactly.