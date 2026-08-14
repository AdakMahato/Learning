import streamlit as st
from story_data import STORIES
from ui import configure_page, sidebar
configure_page("Achievements · DBMS Story Lab"); sidebar("achievements")
st.markdown('<div class="eyebrow">MILESTONES</div><h1>Achievements</h1><p class="muted">Recognition for the investigations you complete.</p>', unsafe_allow_html=True)
completed=len(st.session_state.completed)
badges=[("First resolution", "Clear your first case", completed >= 1), ("SQL investigator", "Clear both SQL investigations", {1,6}.issubset(st.session_state.completed)), ("Systems thinker", "Clear three distributed or transaction cases", len(st.session_state.completed & {2,5,7,8}) >= 3), ("DBMS scholar", "Clear all 11 investigations", completed == 11)]
for title, detail, unlocked in badges:
    state="Unlocked" if unlocked else "Locked"; icon="✓" if unlocked else "○"
    st.markdown(f'<div class="stat-card" style="margin-bottom:12px"><span class="stat-icon">{icon}</span><div style="font-weight:700;color:#172033">{title}</div><div class="stat-label">{detail} · {state}</div></div>', unsafe_allow_html=True)
