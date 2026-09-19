v1.40.23 — interaction + portrait UI crash bisect

error.log signature at crash:
  Character -4294967295 (invalid scope)
  POD_no_beauty_trait_makeup_trigger scope: none
  portrait_frankish_unique_haircut scope: none

Changes:
1. ALL CoS character_interactions disabled (moved here)
2. POD_no_beauty_trait_makeup_trigger + POD_disable_ainu_makeup_trigger
   — exists=this overrides in POD_portrait/zz_lasombra_court_pod_portrait_skin_fix.txt
3. is_naked apply = no-op (clear-only) in 17_lasombra_court_portrait_effects.txt

RESTORED in v1.40.24: 02_lasombra_court_umbral_council_interactions.txt
RESTORED in v1.40.30: 05_lasombra_court_question_embrace_interaction.txt
RESTORED in v1.40.38: zz_cosla_grant_lifestyle_access_interaction.txt

Restore remaining interactions one file at a time after right-click + F4 stable.

Workarounds until restored:
  - Council appoint: use decisions / events, not right-click interaction
  - Avoid character screen courtier right-click if still crashing

RESTORED in v1.40.122: 03_lasombra_court_shadow_adoption_interaction.txt (Draw into the Shadow Household)

RESTORED v1.40.126: 04 baptism, 06 umbral crossing. Herd feast retired (not restored).
