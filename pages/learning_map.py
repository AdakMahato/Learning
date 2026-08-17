import streamlit as st
from story_data import STORIES
from ui import ACCENTS, CATEGORIES, configure_page, sidebar, story_status

configure_page("Learning Map · DBMS Story Lab")
sidebar("map")

st.markdown(
    '<div class="eyebrow">CURRICULUM OVERVIEW</div>'
    '<h1>Learning Map</h1>'
    '<p class="muted">A recommended path through the DBMS curriculum — from foundations to distributed systems.</p>',
    unsafe_allow_html=True,
)

# ── Recommended linear path ────────────────────────────────────────────────────
RECOMMENDED_PATH = [9, 10, 4, 11, 1, 3, 6, 5, 8, 2, 7]
story_by_id = {s["id"]: s for s in STORIES}

st.markdown('<div class="section-title">Recommended path</div>', unsafe_allow_html=True)

path_html = (
    '<div style="display:flex;align-items:center;flex-wrap:wrap;gap:6px;'
    'padding:16px 20px;background:#FFF;border:1px solid #E4E7EC;border-radius:14px;margin-bottom:2rem;">'
)
for i, sid in enumerate(RECOMMENDED_PATH):
    s = story_by_id[sid]
    status, _ = story_status(sid)
    is_done = "Completed" in status
    is_wip = "progress" in status.lower()
    color = "#15803D" if is_done else "#4338CA" if is_wip else "#98A2B3"
    bg = "#F0FDF4" if is_done else "#EEF2FF" if is_wip else "#F9FAFB"
    border = "#BBF7D0" if is_done else "#C7D2FE" if is_wip else "#E4E7EC"
    badge = "✓" if is_done else "◐" if is_wip else str(sid)
    path_html += (
        f'<span style="display:inline-flex;flex-direction:column;align-items:center;'
        f'gap:3px;background:{bg};border:1px solid {border};border-radius:10px;'
        f'padding:8px 10px;min-width:70px;">'
        f'<span style="font-size:1.1rem">{s["icon"]}</span>'
        f'<span style="font-size:.68rem;font-weight:700;color:{color}">{badge}</span>'
        f'<span style="font-size:.65rem;color:#667085;text-align:center;line-height:1.3">'
        f'{s["title"].split(" ")[1] if len(s["title"].split(" ")) > 1 else s["title"][:8]}</span>'
        f'</span>'
    )
    if i < len(RECOMMENDED_PATH) - 1:
        path_html += '<span style="color:#D0D5DD;font-size:1rem;margin:0 2px">→</span>'
path_html += "</div>"
st.markdown(path_html, unsafe_allow_html=True)

# ── Tracks ─────────────────────────────────────────────────────────────────────
TRACKS = [
    ("Foundation", "Start here — why DBMS exist", [9]),
    ("Design & Modeling", "ER diagrams, normalization, relational theory", [10, 4, 11]),
    ("SQL Mastery", "Query, investigate, and analyze", [1, 6]),
    ("Performance", "Indexes, query plans, and OLAP", [3]),
    ("Transactions", "Concurrency, locking, and MVCC", [5, 8]),
    ("Distributed Systems", "Replication, consensus, and CAP", [2, 7]),
]

st.markdown('<div class="section-title">By track</div>', unsafe_allow_html=True)

for track_name, track_desc, track_ids in TRACKS:
    done_count = sum(1 for sid in track_ids if sid in st.session_state.completed)
    total_count = len(track_ids)

    cards_html = ""
    for sid in track_ids:
        s = story_by_id[sid]
        status, _ = story_status(sid)
        accent = ACCENTS[sid]
        is_done = "Completed" in status
        is_wip = "progress" in status.lower()
        bg = "#F0FDF4" if is_done else "#EEF2FF" if is_wip else "#FAFAFA"
        border = "#BBF7D0" if is_done else "#C7D2FE" if is_wip else "#E4E7EC"
        status_color = "#15803D" if is_done else "#4338CA" if is_wip else "#98A2B3"
        status_label = "✓ Done" if is_done else "◐ In progress" if is_wip else "○ Open"
        cards_html += (
            f'<div style="background:{bg};border:1px solid {border};border-radius:12px;'
            f'padding:16px;flex:1;min-width:160px;max-width:260px;">'
            f'<div style="font-size:1.3rem;margin-bottom:8px">{s["icon"]}</div>'
            f'<div style="font-size:.7rem;font-weight:700;letter-spacing:.07em;color:{accent};margin-bottom:4px">'
            f'{CATEGORIES[sid].upper()}</div>'
            f'<div style="font-weight:600;color:#172033;font-size:.9rem;margin-bottom:5px;line-height:1.35">'
            f'{s["title"]}</div>'
            f'<div style="color:#98A2B3;font-size:.72rem;margin-bottom:10px">{s["difficulty"]}</div>'
            f'<div style="color:#475467;font-size:.74rem;margin-bottom:10px;line-height:1.4">{s["hook"]}</div>'
            f'<div style="font-size:.73rem;font-weight:700;color:{status_color}">{status_label}</div>'
            f'</div>'
        )

    progress_color = "#15803D" if done_count == total_count else "#4F46E5"
    badge_bg = "#F0FDF4" if done_count == total_count else "#EEF2FF"
    badge_color = "#15803D" if done_count == total_count else "#4338CA"

    track_html = (
        f'<div style="background:#FFF;border:1px solid #E4E7EC;border-radius:14px;'
        f'padding:20px;margin-bottom:14px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;">'
        f'<div>'
        f'<div style="font-weight:700;color:#172033;font-size:1.05rem;letter-spacing:-.02em">{track_name}</div>'
        f'<div style="color:#667085;font-size:.82rem;margin-top:3px">{track_desc}</div>'
        f'</div>'
        f'<div style="background:{badge_bg};border-radius:999px;padding:4px 12px;'
        f'font-size:.76rem;font-weight:700;color:{badge_color};white-space:nowrap">'
        f'{done_count}/{total_count} done</div>'
        f'</div>'
        f'<div style="display:flex;gap:12px;flex-wrap:wrap;">'
        f'{cards_html}'
        f'</div></div>'
    )
    st.markdown(track_html, unsafe_allow_html=True)

# ── Prerequisites ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Prerequisites guide</div>', unsafe_allow_html=True)

PREREQS = [
    ("01 · The Vanishing Hour", "Basic SQL familiarity helpful (SELECT, FROM, WHERE)"),
    ("03 · Silence Between Signals", "Complete Story 01 first — indexes build on SQL intuition"),
    ("05 · The Last Broadcast", "Complete Story 01 first — transactions build on query knowledge"),
    ("08 · The Machine That Lied", "Complete Story 05 — MVCC extends locking and isolation concepts"),
    ("07 · Colony Forgot Its Laws", "Complete Story 02 — consensus extends CAP and replication"),
    ("11 · The Impossible Contract", "Complete Story 04 — 5NF builds directly on BCNF"),
]

prereq_html = (
    '<div style="background:#FFF;border:1px solid #E4E7EC;border-radius:14px;'
    'padding:8px 20px;margin-bottom:2rem;">'
)
for title, prereq in PREREQS:
    prereq_html += (
        f'<div style="display:flex;gap:16px;padding:12px 0;border-bottom:1px solid #F2F4F7;align-items:flex-start;">'
        f'<div style="font-weight:600;color:#172033;font-size:.86rem;min-width:220px;flex-shrink:0">{title}</div>'
        f'<div style="color:#667085;font-size:.84rem;line-height:1.45">{prereq}</div>'
        f'</div>'
    )
prereq_html += "</div>"
st.markdown(prereq_html, unsafe_allow_html=True)

# ── XP table ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">XP per level</div>', unsafe_allow_html=True)
level_names = ["Discovery", "Investigation", "Complexity", "Failure",
               "Optimization", "Conflict", "Disaster", "Final Boss"]
level_xp = [20, 25, 30, 35, 40, 45, 50, 100]
xp_html = (
    '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:2rem;">'
)
for name, xp in zip(level_names, level_xp):
    xp_html += (
        f'<div style="background:#FFF;border:1px solid #E4E7EC;border-radius:10px;'
        f'padding:12px 16px;text-align:center;min-width:90px;flex:1;">'
        f'<div style="font-size:.72rem;font-weight:700;color:#667085;letter-spacing:.05em">{name.upper()}</div>'
        f'<div style="font-size:1.2rem;font-weight:700;color:#4F46E5;margin-top:4px">+{xp}</div>'
        f'<div style="font-size:.68rem;color:#98A2B3">XP</div>'
        f'</div>'
    )
xp_html += "</div>"
st.markdown(xp_html, unsafe_allow_html=True)

total_xp = sum(level_xp) * 11
st.markdown(
    f'<p class="muted" style="text-align:center;margin-bottom:2rem">'
    f'Complete all 11 stories to earn up to <b style="color:#172033">{total_xp:,} XP</b> total.</p>',
    unsafe_allow_html=True,
)
