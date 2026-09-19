v1.40.21 — KISS portrait / nudity strip (stability pass)

Disabled (moved from gfx/portraits/portrait_modifiers/):
  lasombra_court_salon_hair.txt
  lasombra_court_umbral_portrait.txt
  lasombra_court_activity_revel_portrait.txt

Kept instead:
  common/scripted_triggers/POD_portrait/zz_lasombra_court_pod_portrait_triggers.txt
    — load-order override of POD_portrait_nun_habit_trigger (no umbral_portrait modifier needed)

Nudity (v1.40.21):
  vanilla is_naked flag only (17_lasombra_court_portrait_effects.txt)
  active: Umbral Crossing + consort introduction event chains
  deferred: activity revel attire, umbral orgy map-wide nudity

Restore later (after stable): move files back to gfx/portraits/portrait_modifiers/
or reintroduce Natural Primitivism / event outfit_tags per Sappho pattern.