v1.40.10 diagnostic strip — CoS "surface" assets disabled for crash bisection.

Council GUI was removed in v1.40.9; crash persisted with same signature:
  - 3x Character -4294967295 at map load (Script location: Unknown)
  - ~10s later: portrait modifiers run with scope NONE → custom_hair / POD_no_beauty spam → hard crash

Disabled in this strip (moved here, not deleted):
  gui/ — all overrides (lifestyle, activity planner, ruler designer, chargen faith widget, shared types)
  gfx/portraits/portrait_modifiers/ — salon_hair, umbral_portrait, activity_revel
  data_binding/zz_lasombra_court_data_bindings.txt
  common/important_actions/zz_lasombra_court_*.txt

Still active: culture, faith, events, on_action, council tasks (script), decisions, activities.

If v1.40.10 is STABLE → crash is in one of the disabled surface files; restore one at a time.
If v1.40.10 still CRASHES → bisect on_action / events / portrait triggers next.