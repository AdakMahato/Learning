"""
persistence.py
--------------
Save and restore user progress to/from a local SQLite database.
"""
import sqlite3
import json
import os
import streamlit as st

DB_FILE = os.path.join(os.path.dirname(__file__), "progress.db")

def _get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY,
            xp INTEGER,
            completed TEXT,
            mission_state TEXT
        )
    ''')
    return conn

def load_progress():
    """Inject saved progress into session state. Runs only once per session."""
    if st.session_state.get("_progress_loaded"):
        return
    st.session_state["_progress_loaded"] = True

    # Initialize defaults
    if "xp" not in st.session_state:
        st.session_state.xp = 0
    if "completed" not in st.session_state:
        st.session_state.completed = set()

    conn = _get_conn()
    try:
        row = conn.execute('SELECT xp, completed, mission_state FROM user_progress WHERE id = 1').fetchone()
        if row:
            xp, completed_json, mission_state_json = row
            st.session_state.xp = xp
            try:
                st.session_state.completed = set(json.loads(completed_json))
            except:
                pass
            
            try:
                mission_state = json.loads(mission_state_json)
                for k, v in mission_state.items():
                    if isinstance(v, list) and (k.startswith("completed_levels_") or k == "notebook_seen"):
                        st.session_state[k] = set(v)
                    else:
                        st.session_state[k] = v
            except:
                pass
    except Exception:
        pass
    finally:
        conn.close()

def save_progress():
    """Persist the current session state to progress.db."""
    mission_state = {}
    for k, v in st.session_state.items():
        if k.startswith(("mission_", "completed_levels_", "active_level_", "notebook_")):
            if isinstance(v, set):
                mission_state[k] = list(v)
            else:
                mission_state[k] = v

    xp = st.session_state.get("xp", 0)
    completed_json = json.dumps(list(st.session_state.get("completed", set())))
    mission_state_json = json.dumps(mission_state)

    try:
        conn = _get_conn()
        conn.execute('''
            INSERT OR REPLACE INTO user_progress (id, xp, completed, mission_state)
            VALUES (1, ?, ?, ?)
        ''', (xp, completed_json, mission_state_json))
        conn.commit()
        conn.close()
    except Exception:
        pass
