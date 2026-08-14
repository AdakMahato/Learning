import pandas as pd
import streamlit as st
from story_data import STORIES
from ui import CATEGORIES, configure_page, sidebar, story_status
configure_page("Learning map · DBMS Story Lab"); sidebar("map")
st.markdown('<div class="eyebrow">CURRICULUM OVERVIEW</div><h1>Learning map</h1><p class="muted">A sequenced path from DBMS foundations to distributed systems.</p>', unsafe_allow_html=True)
rows=[]
for story in STORIES:
    status,_ = story_status(story["id"]); rows.append({"Case":f"{story['id']:02d}. {story['title']}","Track":CATEGORIES[story['id']],"Focus":story['primary'],"Status":status})
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
