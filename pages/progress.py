import pandas as pd
import streamlit as st
from story_data import STORIES
from ui import configure_page, sidebar, skill_radar

configure_page("Progress dossier · DBMS Story Lab")
sidebar("progress")
st.markdown('<div class="eyebrow">YOUR LEARNING RECORD</div><h1>Progress</h1><p class="muted">Your progress across the DBMS curriculum.</p>', unsafe_allow_html=True)
one, two = st.columns(2)
one.metric("XP earned", st.session_state.xp)
two.metric("Stories cleared", f"{len(st.session_state.completed)} / 11")
rows = [{"Case": f"{s['id']:02d}. {s['title']}", "Focus": s['primary'], "Status": "✓ Cleared" if s['id'] in st.session_state.completed else "○ Open"} for s in STORIES]
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
st.markdown('<div class="section-title">Skill profile</div>', unsafe_allow_html=True)
st.plotly_chart(skill_radar(), use_container_width=True, config={"displayModeBar": False})
