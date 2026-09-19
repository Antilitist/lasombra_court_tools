"""Build per-activity Court of Shadows notification icons (432x144, 3 alert states)."""
import importlib.util
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(TOOLS, "..", "lasombra_court"))

ACTIVITY_ALERTS = {
    "action_can_host_lasombra_court_black_chapel_procession": os.path.join(
        TOOLS, "source_task_legate_sanctify_chapels.jpg"
    ),
    "action_can_host_lasombra_court_veiled_pursuit": os.path.join(
        TOOLS, "source_task_curator_tempt_heart.jpg"
    ),
    # Vanilla auto-action key is action_can_host_<full activity type>
    "action_can_host_activity_lasombra_court_nox_tenebrarum_pilgrimage": os.path.join(
        TOOLS, "source_nox_tenebrarum_pilgrimage.jpg"
    ),
}


def load_decision_icon_builder():
    path = os.path.join(TOOLS, "convert_decision_alert_icon.py")
    spec = importlib.util.spec_from_file_location("convert_decision_alert_icon", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    builder = load_decision_icon_builder()
    for icon_name, art_path in ACTIVITY_ALERTS.items():
        if not os.path.isfile(art_path):
            raise FileNotFoundError(art_path)
        builder.build_alert_icon(icon_name, art_path)


if __name__ == "__main__":
    main()