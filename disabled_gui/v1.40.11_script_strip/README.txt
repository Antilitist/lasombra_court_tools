v1.40.11 — script-layer strip (on top of v1.40.10 surface strip).

v1.40.10 result: ~2+ min idle before crash (up from ~47 sec). Surface assets
were contributing but not sole cause.

Disabled here:
  common/on_action/* — all 14 hooks (game_start, council pulses, sanitize,
    embrace petition, salon lifestyle, RD finished, etc.)
  common/scripted_triggers/POD_portrait/zz_lasombra_court_pod_portrait_triggers.txt
    — global overrides of POD_portrait_nun_habit_trigger / portrait_monk_robe

Still active from v1.40.10 strip: no GUI overrides, no portrait modifiers,
no important_actions, no data_bindings.

If STABLE → re-enable on_action first, then POD portrait triggers, one file at a time.
If CRASHES → bisect events / council positions / lifestyle data next.