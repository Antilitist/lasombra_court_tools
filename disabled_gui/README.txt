v1.40.9 — window_council.gui moved here (not deleted).

Why: visible=no kill-switch (v1.40.8) still loads the override file; Jomini
evaluates datacontext/bindings even on hidden widgets. The 3x Character
-4294967295 errors at map load persisted with the kill-switch.

Restoring umbral council UI later:
1. Copy v1.40.9_window_council.gui.bak back to gui/window_council.gui
2. Remove the v1.40.8 root visible=no kill-switch
3. Fix 3-arg And() on my_council visible — use nested And( And(A,B), C )
4. Gate umbral council datacontext behind LasombraCourtPlayerGuiReady + Character.IsValid