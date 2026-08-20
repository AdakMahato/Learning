import streamlit as st
from story_data import STORIES
from ui import CATEGORIES, configure_page, sidebar, story_card

configure_page()
sidebar("home")
st.markdown('''<div class="hero"><div class="eyebrow">INTERACTIVE DBMS CURRICULUM</div><h1>DBMS Story Lab</h1><p>Learn database systems by solving problems,<br>not memorizing definitions.</p><p style="font-size:.86rem;margin-top:.85rem">Foundation + 11 investigations &nbsp;•&nbsp; Interactive labs &nbsp;•&nbsp; Progressive difficulty</p></div>''', unsafe_allow_html=True)

st.markdown('''<div style="background:#EEF2FF; border:1px solid #C7D2FE; border-radius:12px; padding:25px; margin-bottom: 20px;">
<div style="color:#4F46E5; font-size:.74rem; font-weight:750; letter-spacing:.11em; margin-bottom: 8px;">🚀 START HERE</div>
<h2 style="margin: 0 0 10px 0; color:#172033;">The Database Behind the World</h2>
<p style="color:#475467; margin-bottom: 15px;">New to DBMS? Start here. Build your mental model before entering the investigations.</p>
</div>''', unsafe_allow_html=True)
if st.button("Enter the Foundation →", key="enter_foundation", type="primary"):
    st.switch_page("pages/00_foundation.py")

st.markdown('<div class="section-title">Your investigations</div>', unsafe_allow_html=True)
search_col, filter_col = st.columns([8, 1])
with search_col:
    search = st.text_input("Search investigations", placeholder="Search investigations…", label_visibility="collapsed")
filters = ["All", "Foundation", "SQL", "Design", "Performance", "Transactions", "Distributed Systems"]
with filter_col:
    with st.popover("☰ Filters", use_container_width=True):
        selected = st.radio("Filter by track", filters, label_visibility="visible")
query = search.strip().lower()
def matches(story):
    if story["id"] == 0: return False
    haystack = " ".join([story["title"], story["hook"], story["genre"], story["difficulty"], " ".join(story["topics"]), CATEGORIES[story["id"]]]).lower()
    return (selected == "All" or CATEGORIES[story["id"]] == selected) and (not query or query in haystack)
visible = [s for s in STORIES if matches(s)]
if not visible: st.info("No investigations match that search. Try a topic, story title, or difficulty.")
for start in range(0, len(visible), 3):
    cols = st.columns(3)
    for col, story in zip(cols, visible[start:start + 3]):
        with col: story_card(story)
st.markdown('<div class="section-title">A guided learning path</div>', unsafe_allow_html=True)
st.markdown('<p class="muted">Build foundations first, then move through modeling, SQL, performance, transactions, and distributed systems. Your detailed skill profile is available in Progress.</p>', unsafe_allow_html=True)
