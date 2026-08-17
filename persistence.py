"""
persistence.py
--------------
Save and restore user progress to/from a local JSON file.
No extra dependencies — uses stdlib json + os only.
"""
import json
import os

import streamlit as st

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "progress.json")


def load_progress():
    """Inject saved progress into session state. Runs only once per session."""
    if st.session_state.get("_progress_loaded"):
        return
    st.session_state["_progress_loaded"] = True

    if not os.path.exists(PROGRESS_FILE):
        return

    try:
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)

        st.session_state["xp"] = data.get("xp", 0)
        st.session_state["completed"] = set(data.get("completed", []))

        # Restore per-story level sets (stored as lists in JSON)
        for key, value in data.get("level_progress", {}).items():
            st.session_state[key] = set(value)

        # Restore misc per-story scalars (active_level_*, etc.)
        for key, value in data.get("misc", {}).items():
            if key not in st.session_state:
                st.session_state[key] = value

    except Exception:
        # Corrupt or unreadable file — silently start fresh
        pass


def save_progress():
    """Persist the current session state to progress.json."""
    level_progress = {}
    misc = {}

    for key, value in st.session_state.items():
        if key.startswith("completed_levels_"):
            level_progress[key] = list(value) if isinstance(value, set) else value
        elif key.startswith("active_level_"):
            misc[key] = value

    data = {
        "xp": st.session_state.get("xp", 0),
        "completed": list(st.session_state.get("completed", set())),
        "level_progress": level_progress,
        "misc": misc,
    }

    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        # File system error — skip silently
        pass
