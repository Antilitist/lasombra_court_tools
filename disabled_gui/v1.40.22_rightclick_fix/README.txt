v1.40.22 — right-click / interaction wheel crash fix

Cause: redirect blocks rewrote scope:recipient during interaction menu build,
corrupting the portrait datacontext (scope: none → hard crash).

Fixes:
1. shadow_adoption — pick_custodian only when child_shown_trigger (not every right-click)
2. POD portrait triggers — exists = this guard on all three overrides
3. child_study_language override DISABLED — redirect swapped recipient to employer
   on every courtier right-click when Court Tutor employed; restore after rewrite

Test: right-click courtiers on map + in court view; avoid F4 council tab still.

v1.40.123: Ward language restored as NEW interaction lasombra_court_ward_study_language_interaction (no vanilla override, no recipient redirect). Old zz override stays disabled.

v1.40.124: Safe vanilla override zz_lasombra_court_make_child_learn_language.txt — family OR ward, no employer recipient rewrite.
