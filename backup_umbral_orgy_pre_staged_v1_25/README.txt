Umbral Orgy — pre-staged-chain backup (v1.24.0 baseline)
=========================================================

Created before v1.25.0 staged Saturnalia event chain.

To restore the old single-beat flow (0198 -> 0200 -> 0201):
  1. Copy files from this folder back into the mod root (preserve paths).
  2. Remove common/scripted_effects/11_lasombra_court_umbral_orgy_chain_effects.txt if present.
  3. Revert lasombra_court.mod version if desired.

Files backed up:
  events/02_lasombra_court_umbral_orgy_events.txt
  events/07_lasombra_court_orgy_aftermath_events.txt
  common/scripted_effects/01_lasombra_court_umbral_orgy_effects.txt
  common/scripted_effects/02_lasombra_court_umbral_orgy_summary_effects.txt
  common/scripted_effects/03_lasombra_court_umbral_orgy_invite_effects.txt
  common/scripted_effects/06_lasombra_court_umbral_orgy_tally_effects.txt
  common/decisions/00_lasombra_court_decisions.txt

Old chain: decision -> 0198 summons -> 0200 (all simulation in immediate) -> 0201 ledger

New chain (v1.25.0): decision -> 0198 -> 0205 -> 0206 -> 0207 -> 0208 -> 0209 -> 0213 -> 0214 -> 0201
New file NOT in backup (remove on restore): common/scripted_effects/11_lasombra_court_umbral_orgy_chain_effects.txt
Legacy monolith 0200 retained in live mod for console testing only.