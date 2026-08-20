import streamlit as st

from challenges import render_story_challenge
from story_data import STORIES
from persistence import load_progress, save_progress
from level_content import LEVEL_CONTENT

PAGE_PATHS = {0: "pages/00_foundation.py", 1: "pages/01_vanishing_hour.py", 2: "pages/02_convoy_zero.py", 3: "pages/03_silence_between_signals.py", 4: "pages/04_remembered_too_much.py", 5: "pages/05_last_broadcast.py", 6: "pages/06_depth_ledger.py", 7: "pages/07_colony_laws.py", 8: "pages/08_machine_lied.py", 9: "pages/09_forgotten_archive.py", 10: "pages/10_impossible_blueprint.py", 11: "pages/11_impossible_contract.py"}
ACCENTS = {0: "#047857", 1: "#7C3AED", 2: "#2563EB", 3: "#0891B2", 4: "#9333EA", 5: "#DC2626", 6: "#B45309", 7: "#059669", 8: "#4F46E5", 9: "#64748B", 10: "#0F766E", 11: "#B45309"}
CATEGORIES = {0: "Foundation", 1: "SQL", 2: "Distributed Systems", 3: "Performance", 4: "Design", 5: "Transactions", 6: "SQL", 7: "Distributed Systems", 8: "Transactions", 9: "Foundation", 10: "Design", 11: "Design"}


def configure_page(title="DBMS Story Lab"):
    st.set_page_config(page_title=title, page_icon="🗄️", layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    .stApp { background:#F7F8FA; color:#172033; }
    .block-container { max-width:1400px; padding:5.7rem 3rem 3.5rem; }
    [data-testid="stSidebar"] { background:#FFFFFF; border-right:1px solid #E4E7EC; }
    [data-testid="stSidebar"] > div:first-child { padding:1.2rem .8rem; }
    [data-testid="stSidebarNav"] { display:none; }
    #MainMenu, footer, header { visibility:hidden; }
    .brand { padding:.45rem .6rem 1.4rem; }
    .brand-title { color:#172033; font-weight:700; font-size:1.1rem; letter-spacing:-.02em; }
    .brand-subtitle, .muted { color:#667085; font-size:.81rem; }
    .nav-label { color:#98A2B3; font-weight:700; letter-spacing:.09em; font-size:.67rem; margin:1.35rem .55rem .35rem; }
    [data-testid="stSidebar"] a[data-testid="stPageLink-Nav"] { color:#475467; border-radius:8px; min-height:38px; padding:8px 10px; margin:2px 0; font-size:.9rem; transition: background 180ms ease, color 180ms ease; }
    [data-testid="stSidebar"] a[data-testid="stPageLink-Nav"]:hover { background:#F2F4F7; color:#172033; }
    [data-testid="stSidebar"] a[data-testid="stPageLink-Nav"] p { font-weight:500; }
    .nav-active { background:#EEF2FF; color:#4338CA !important; border-radius:8px; padding:9px 10px; font-weight:650; font-size:.9rem; margin:2px 0; }
    .sidebar-bottom { border-top:1px solid #E4E7EC; margin-top:2rem; padding:.95rem .55rem 0; }
    .sidebar-stat { color:#172033; font-size:.82rem; font-weight:650; margin:0 0 .25rem; }
    .sidebar-xp { color:#667085; font-size:.78rem; margin-top:.9rem; }
    .global-status-bar { position:fixed; top:0; left:0; right:0; z-index:9999; height:60px; display:flex; align-items:center; justify-content:center; background:#FFF; border-bottom:1px solid #E4E7EC; box-shadow:0 2px 8px rgba(16,24,40,.04); }
    .global-status-inner { width:min(760px, 100%); display:grid; grid-template-columns:repeat(3, 1fr); height:100%; } .global-status-item { display:flex; justify-content:center; align-items:center; gap:8px; color:#667085; font-size:.84rem; border-right:1px solid #EAECF0; } .global-status-item:last-child { border-right:0; } .global-status-item b { color:#172033; font-size:1.05rem; letter-spacing:-.02em; }
    .global-status-icon { color:#4F46E5; font-size:.88rem; }
    .hero { padding:.5rem 0 1.8rem; max-width:650px; }
    .eyebrow { color:#4F46E5; font-size:.74rem; font-weight:750; letter-spacing:.11em; }
    .hero h1 { color:#172033; font-size:3rem; line-height:1.12; letter-spacing:-.045em; margin:.55rem 0 .65rem; }
    .hero p { color:#667085; font-size:1.08rem; line-height:1.6; margin:0; }
    .section-title { font-size:1.5rem; letter-spacing:-.025em; margin:2.1rem 0 .85rem; }
    .stat-card { background:#FFF; border:1px solid #E4E7EC; border-radius:12px; padding:18px 20px; min-height:104px; box-shadow:0 1px 2px rgba(16,24,40,.03); }
    .stat-icon { color:#4F46E5; float:right; font-size:1.1rem; }
    .stat-value { color:#172033; font-weight:700; font-size:1.65rem; letter-spacing:-.04em; margin-top:10px; }
    .stat-label { color:#667085; font-size:.84rem; margin-top:2px; }
    .story-card { background:#FFF; border:1px solid #E4E7EC; border-radius:14px; padding:18px; height:306px; display:flex; flex-direction:column; box-sizing:border-box; box-shadow:0 1px 2px rgba(16,24,40,.03); transition:transform 180ms ease,box-shadow 180ms ease,border-color 180ms ease; }
    .story-card:hover { transform:translateY(-4px); box-shadow:0 12px 30px rgba(16,24,40,.10); border-color:#C7D2FE; }
    .story-icon { width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.35rem; margin-bottom:14px; }
    .story-category { color:#667085; font-size:.74rem; font-weight:650; margin-bottom:5px; }
    .story-card h3 { color:#172033; font-size:1.1rem; letter-spacing:-.02em; margin:0 0 7px; }
    .story-desc { color:#667085; font-size:.86rem; line-height:1.45; margin:0; min-height:50px; }
    .badges { margin-top:14px; min-height:29px; }
    .badge { display:inline-block; background:#F2F4F7; border-radius:999px; color:#475467; padding:4px 8px; margin:2px 3px 2px 0; font-size:.68rem; font-weight:600; }
    .card-footer { border-top:1px solid #F2F4F7; margin-top:auto; padding-top:11px; color:#667085; font-size:.72rem; font-weight:650; letter-spacing:.025em; }
    .status-complete { color:#15803D; } .status-progress { color:#D97706; } .status-open { color:#667085; }
    .stButton > button { background:#FFF; border:1px solid #E4E7EC; color:#4338CA; border-radius:8px; font-weight:650; min-height:38px; transition:all 180ms ease; box-shadow:none; }
    .stButton > button:hover { background:#EEF2FF; border-color:#C7D2FE; color:#3730A3; }
    .stTextInput input { background:#FFF; border:1px solid #D0D5DD; border-radius:8px; min-height:42px; }
    .stTextInput input:focus { border-color:#818CF8; box-shadow:0 0 0 3px #EEF2FF; }
    [data-testid="stPopover"] > button { background:#FFF; border:1px solid #D0D5DD; color:#344054; border-radius:8px; min-height:42px; font-weight:600; white-space:nowrap; }
    [data-testid="stPopover"] > button:hover { background:#F9FAFB; border-color:#C7D2FE; color:#4338CA; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid #E4E7EC; }
    .stTabs [data-baseweb="tab"] { color:#667085; padding:10px 12px; } .stTabs [aria-selected="true"] { color:#4338CA !important; font-weight:650; }
    .case-header { background:#FFF; border:1px solid #E4E7EC; border-radius:14px; padding:26px; margin:.6rem 0 1.5rem; }
    .level-row { display:flex; gap:8px; flex-wrap:wrap; margin:1rem 0; }
    .level { border:1px solid #E4E7EC; color:#667085; border-radius:8px; padding:7px 9px; font-size:.76rem; } .level.active { color:#4338CA; border-color:#C7D2FE; background:#EEF2FF; font-weight:650; } .level.done { color:#15803D; border-color:#BBF7D0; background:#F0FDF4; }
    @media (max-width: 900px) { .block-container { padding:5rem 1.2rem 2.5rem; } .hero h1 { font-size:2.35rem; } .story-card { height:320px; } } @media (max-width:600px) { .global-status-item { gap:4px; font-size:.72rem; } .global-status-item b { font-size:.9rem; } .global-status-icon { display:none; } }
    </style>
    """, unsafe_allow_html=True)
    ensure_state()
    completed = len(st.session_state.completed)
    st.markdown(f'''<div class="global-status-bar"><div class="global-status-inner"><div class="global-status-item"><span class="global-status-icon">▣</span><b>11</b><span>Investigations</span></div><div class="global-status-item"><span class="global-status-icon">✓</span><b>{completed} / 11</b><span>Completed</span></div><div class="global-status-item"><span class="global-status-icon">✦</span><b>{st.session_state.xp:,}</b><span>XP earned</span></div></div></div>''', unsafe_allow_html=True)


def ensure_state():
    load_progress()  # Restore saved progress on first call; no-op on subsequent calls
    st.session_state.setdefault("completed", set())
    st.session_state.setdefault("xp", 0)
    st.session_state.setdefault("missions", {})


def mark_complete(story_id, amount=100, level=1, total_levels=1):
    key = f"mission_{story_id}_{level}"
    if not st.session_state.get(key):
        st.session_state[key] = True
        st.session_state.xp += amount
        if level == total_levels:
            st.session_state.completed.add(story_id)
        save_progress()


def skill_radar():
    import plotly.graph_objects as go
    categories = ["SQL", "Modeling", "Normalization", "Indexing", "Transactions", "Concurrency", "Distributed", "Recovery"]
    base = [35, 30, 28, 25, 25, 24, 20, 22]
    cleared = len(st.session_state.completed)
    values = [min(100, score + cleared * 5) for score in base]
    fig = go.Figure(go.Scatterpolar(r=values + values[:1], theta=categories + categories[:1], fill="toself", fillcolor="rgba(79,70,229,.12)", line={"color": "#4F46E5", "width": 2}))
    fig.update_layout(paper_bgcolor="#FFFFFF", font_color="#475467", showlegend=False, height=360, margin={"l":45,"r":45,"t":25,"b":25}, polar={"bgcolor":"#FFFFFF", "radialaxis":{"visible":True,"range":[0,100],"gridcolor":"#E4E7EC","linecolor":"#E4E7EC"}, "angularaxis":{"gridcolor":"#E4E7EC","linecolor":"#E4E7EC"}})
    return fig


def sidebar(active="home"):
    with st.sidebar:
        st.markdown('<div class="brand"><div class="brand-title">DBMS Story Lab</div><div class="brand-subtitle">Interactive DBMS Curriculum</div></div>', unsafe_allow_html=True)
        if active == "home": st.markdown('<div class="nav-active">⌂ &nbsp; Home</div>', unsafe_allow_html=True)
        else: st.page_link("app.py", label="⌂  Home")
        st.markdown('<div class="nav-label">LEARN</div>', unsafe_allow_html=True)
        if active == "map": st.markdown('<div class="nav-active">◈ &nbsp; Learning Map</div>', unsafe_allow_html=True)
        else: st.page_link("pages/learning_map.py", label="◈  Learning Map")
        if active == "notebook": st.markdown('<div class="nav-active">📓 &nbsp; Field Notebook</div>', unsafe_allow_html=True)
        else: st.page_link("pages/12_field_notebook.py", label="📓  Field Notebook")
        st.markdown('<div class="nav-label">PROGRESS</div>', unsafe_allow_html=True)
        if active == "progress": st.markdown('<div class="nav-active">◉ &nbsp; Progress</div>', unsafe_allow_html=True)
        else: st.page_link("pages/progress.py", label="◉  Progress")
        if active == "achievements": st.markdown('<div class="nav-active">★ &nbsp; Achievements</div>', unsafe_allow_html=True)
        else: st.page_link("pages/achievements.py", label="★  Achievements")
        total = len(st.session_state.completed)
        st.markdown(f'<div class="sidebar-bottom"><div class="sidebar-stat">Progress &nbsp; {total} / 11</div></div>', unsafe_allow_html=True)
        st.progress(total / 11)
        st.markdown(f'<div class="sidebar-xp">XP<br><strong style="color:#172033;font-size:1rem">{st.session_state.xp:,}</strong></div>', unsafe_allow_html=True)
        if st.button("Reset progress", use_container_width=True):
            st.session_state.completed = set()
            st.session_state.xp = 0
            st.session_state.missions = {}
            for key in list(st.session_state.keys()):
                if key.startswith(("completed_levels_", "active_level_", "mcq_", "proceed_")):
                    del st.session_state[key]
            save_progress()
            st.rerun()


def story_status(story_id):
    if story_id in st.session_state.completed: return "✓ Completed", "status-complete"
    if any(st.session_state.get(f"mission_{story_id}_{i}") for i in range(1, 9)): return "◐ In progress", "status-progress"
    return "○ Not started", "status-open"


def story_card(story):
    accent = ACCENTS[story["id"]]
    status, status_class = story_status(story["id"])
    badges = "".join(f'<span class="badge">{x}</span>' for x in story["topics"][:3])
    st.markdown(f'''<div class="story-card"><div class="story-icon" style="background:{accent}18">{story['icon']}</div><div class="story-category" style="color:{accent}">{CATEGORIES[story['id']].upper()} · {story['genre']}</div><h3>{story['title']}</h3><p class="story-desc">{story['hook']}</p><div class="badges">{badges}</div><div class="card-footer"><span>{story['difficulty'].upper()}</span><br><span class="{status_class}">{status}</span></div></div>''', unsafe_allow_html=True)
    if st.button("Open investigation →", key=f"enter_{story['id']}", use_container_width=True): st.switch_page(PAGE_PATHS[story["id"]])


LEVELS = [
    ("Discovery", "Read the evidence"), ("Investigation", "Trace the records"),
    ("Complexity", "Test the contradiction"), ("Failure", "Find the weak point"),
    ("Optimization", "Make it scale"), ("Conflict", "Resolve competing facts"),
    ("Disaster", "Recover the truth"), ("Final Boss", "Full reconstruction"),
]
LEVEL_XP = [20, 25, 30, 35, 40, 45, 50, 100]


def workspace_css():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display:none; }
    .workspace-shell { padding-top:8px; } .workspace-rail, .workspace-context { position:sticky; top:74px; align-self:start; max-height:calc(100vh - 86px); overflow-y:auto; }
    .workspace-rail { background:#FFF; border:1px solid #E4E7EC; border-radius:12px; padding:16px 12px; } .workspace-context { background:#FFF; border:1px solid #E4E7EC; border-radius:12px; padding:16px; }
    .rail-title { font-size:.82rem; letter-spacing:.06em; font-weight:800; color:#172033; } .rail-genre { color:#667085; font-size:.74rem; margin:.3rem 0 .65rem; } .rail-mission { color:#475467; font-size:.82rem; line-height:1.45; padding:.75rem 0 1rem; border-top:1px solid #E4E7EC; border-bottom:1px solid #E4E7EC; }
    .rail-label, .context-title, .workspace-eyebrow { color:#667085; font-size:.67rem; letter-spacing:.1em; font-weight:750; margin:1rem 0 .55rem; }
    .level-static { border:1px solid #E4E7EC; border-radius:8px; padding:9px; margin:6px 0; background:#FFF; color:#667085; font-size:.78rem; } .level-static.current { background:#FFF8D6; border-color:#F2C94C; color:#7A5600; } .level-static.done { background:#F8FAFC; color:#344054; } .level-static.locked { opacity:.55; }
    .level-static b { color:#344054; display:block; font-size:.81rem; } .level-static.current b { color:#6B4F00; }
    .workspace-rail .stRadio { margin:.1rem 0 .6rem; } .workspace-rail .stRadio label { font-size:.78rem; }
    .workspace-main { padding:8px 8px 60px; } .workspace-main h1 { color:#172033; font-size:2.2rem; line-height:1.15; letter-spacing:-.04em; margin:.25rem 0 .75rem; } .workspace-main h3 { color:#172033; font-size:.92rem; letter-spacing:.06em; text-transform:uppercase; margin-top:2rem; }
    .objective { background:#F8FAFC; border-left:3px solid #4F46E5; padding:15px 17px; color:#344054; border-radius:0 8px 8px 0; line-height:1.55; }
    .lab-frame { background:#FFF; border:1px solid #E4E7EC; border-radius:12px; padding:18px; margin-top:.6rem; } .lab-frame [data-testid="stTextArea"] textarea { font-family:ui-monospace, SFMono-Regular, Menlo, monospace; background:#101828; color:#E5E7EB; border-color:#101828; border-radius:8px; }
    .context-section { border-top:1px solid #EAECF0; padding:.85rem 0; } .context-section:first-of-type { border-top:0; } .context-table { color:#475467; font-size:.78rem; line-height:1.7; } .context-table b { color:#172033; } .node-online { color:#15803D; } .node-wait { color:#D97706; }
    .hint-box { background:#FFFBEB; border:1px solid #FDE68A; border-radius:9px; padding:12px; color:#713F12; font-size:.88rem; } .success-reveal { background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:15px; color:#166534; }
    @media (max-width:1000px) { .workspace-context { display:none; } .workspace-main { padding-right:0; } } @media (max-width:700px) { .workspace-rail { display:none; } .workspace-main h1 { font-size:1.8rem; } }
    </style>
    """, unsafe_allow_html=True)


def context_panel(story):
    sid = story["id"]
    st.markdown('<div class="context-title">CONTEXT PANEL</div>', unsafe_allow_html=True)
    if sid in (1, 6):
        st.markdown('''<div class="context-section"><div class="context-title">DATABASE</div><div class="context-table"><b>⌄ people</b><br>&nbsp;&nbsp;PK id<br>&nbsp;&nbsp;name<br>&nbsp;&nbsp;city<br><br><b>⌄ sightings</b><br>&nbsp;&nbsp;PK id<br>&nbsp;&nbsp;person_id<br>&nbsp;&nbsp;location<br>&nbsp;&nbsp;event_time<br><br><b>› locations</b></div></div>''', unsafe_allow_html=True)
    elif sid == 3:
        st.markdown('<div class="context-section"><div class="context-title">INDEX LAB</div><div class="context-table">○ No index<br>● <b>event_time</b><br>○ event_time + person_id<br><br>Estimated cost<br><b>18.4s → 0.03s</b></div></div>', unsafe_allow_html=True)
    elif sid in (2, 7):
        st.markdown('<div class="context-section"><div class="context-title">NODES</div><div class="context-table"><span class="node-online">●</span> Veridian-01<br><span class="node-online">●</span> Veridian-02<br><span class="node-wait">●</span> Veridian-03<br><br><b>NETWORK</b><br>A ─── B<br>&nbsp;&nbsp;✕<br>&nbsp;&nbsp;C</div></div>', unsafe_allow_html=True)
    elif sid in (5, 8):
        st.markdown('<div class="context-section"><div class="context-title">TRANSACTIONS</div><div class="context-table">T1 &nbsp;<span class="node-online">● Active</span><br>T2 &nbsp;<span class="node-wait">◐ Waiting</span><br><br><b>LOCKS</b><br>ROW: crate_42<br>X LOCK → T1</div></div>', unsafe_allow_html=True)
    elif sid in (4, 11):
        st.markdown('<div class="context-section"><div class="context-title">SCHEMA</div><div class="context-table"><b>people</b><br>person_id<br>name<br>city<br><br><b>events</b><br>event_id<br>person_id<br>event_time</div></div>', unsafe_allow_html=True)
    elif sid == 10:
        st.markdown('<div class="context-section"><div class="context-title">ENTITIES</div><div class="context-table"><b>Person</b><br><b>Location</b><br><b>Event</b><br><br><b>RELATIONSHIP</b><br>Person ─ sees ─ Location</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="context-section"><div class="context-title">CASE FILE</div><div class="context-table">Evidence fragments: 12<br>Reliable sources: 3<br>Open contradictions: 1<br><br>Record each conclusion in your notes.</div></div>', unsafe_allow_html=True)
    st.divider()
    st.text_area("Scratch notes", key=f"workspace_notes_{sid}", height=130, placeholder="Record a clue…")


def render_episodic_page(story_id, story, data):
    configure_page(f"{story['title']} · DBMS Story Lab")
    workspace_css()
    episodes = data.get("episodes", [])
    completed_episodes = st.session_state.setdefault(f"completed_levels_{story_id}", set())
    active = st.session_state.setdefault(f"active_level_{story_id}", min(len(completed_episodes) + 1, len(episodes)))
    progress = len(completed_episodes)
    hide_context = st.session_state.get(f"hide_context_{story_id}", False)
    widths = [2.25, 6.1, 2.25] if not hide_context else [2.25, 8.35]
    columns = st.columns(widths)
    rail, main = columns[0], columns[1]
    context = columns[2] if not hide_context else None
    
    with rail:
        st.markdown(f'<div class="rail-title">{story["title"].upper()}</div><div class="rail-genre">{story["genre"]}</div><div class="rail-mission">{story["hook"]}</div><div class="rail-label">{len(episodes)} EPISODES</div>', unsafe_allow_html=True)
        available = list(range(1, min(progress + 2, len(episodes) + 1)))
        selected = st.radio("Episodes", available, index=max(0, min(active, len(available)) - 1), format_func=lambda n: f"{n:02d}  Episode {n}", label_visibility="collapsed", key=f"level_picker_{story_id}")
        if selected != active:
            st.session_state[f"active_level_{story_id}"] = selected; st.rerun()
        for number in range(1, len(episodes) + 1):
            if number in available: continue
            st.markdown(f'<div class="level-static locked"><b>🔒 {number:02d} &nbsp; Episode {number}</b></div>', unsafe_allow_html=True)
            
    with main:
        st.markdown('<div class="workspace-main">', unsafe_allow_html=True)
        st.markdown(f'<div class="workspace-eyebrow">EPISODE {active:02d}</div><h1>{story["title"]}</h1>', unsafe_allow_html=True)
        episode_blocks = episodes[active - 1] if active <= len(episodes) else []
        
        def complete_current():
            levels = st.session_state.setdefault(f"completed_levels_{story_id}", set())
            current = st.session_state.get(f"active_level_{story_id}", 1)
            if current not in levels:
                levels.add(current)
                st.session_state.xp += 35
                if current == len(episodes):
                    st.session_state.completed.add(story_id)
            st.session_state[f"active_level_{story_id}"] = min(current + 1, len(episodes))
            save_progress()
            st.rerun()

        from field_notebook import advance_concept
        for i, block in enumerate(episode_blocks):
            btype = block.get("type")
            concept_id = block.get("concept_id")

            if btype == "story":
                st.markdown(f'<div class="objective"><h3>{block.get("title", "")}</h3><p>{block.get("content", block.get("text", ""))}</p></div>', unsafe_allow_html=True)
            elif btype == "problem":
                st.markdown(f'<div style="background:#FEF2F2; border-left:3px solid #EF4444; padding:15px 17px; color:#991B1B; margin: 10px 0; border-radius:0 8px 8px 0;"><b>Problem:</b> {block.get("text", "")}</div>', unsafe_allow_html=True)
            elif btype == "concept":
                if concept_id: advance_concept(concept_id, "INTRODUCED")
                st.markdown(f'<div style="background:#EFF6FF; border:1px solid #BFDBFE; padding:15px; border-radius:10px; margin: 15px 0;"><b>{block.get("title", "")}</b><br><span style="color:#1E3A8A; font-size: 0.9rem;">{block.get("summary", block.get("explanation", ""))}</span></div>', unsafe_allow_html=True)
                if "why_it_matters" in block:
                    st.markdown(f"**Why it matters:** {block['why_it_matters']}")
                if "analogy" in block:
                    st.markdown(f"**Analogy:** {block['analogy']}")
                if "technical_explanation" in block:
                    st.markdown(f"**Technical Detail:** {block['technical_explanation']}")
                if "remember" in block:
                    st.info(f"**Remember:** {block['remember']}")
            elif btype == "visual":
                if concept_id: advance_concept(concept_id, "VISUALIZED")
                if block.get("visual_type") == "code":
                    st.code(block.get("data"), language="text")
                else:
                    st.markdown(f"```text\n{block.get('data')}\n```")
            elif btype == "worked_example":
                if concept_id: advance_concept(concept_id, "PRACTICED")
                st.markdown(f"### {block.get('title')}")
                for step in block.get("steps", []):
                    st.markdown(f"- {step}")
            elif btype == "reflection":
                st.info(f"🤔 **Reflection:** {block.get('question')}")
            elif btype == "micro_challenge":
                st.markdown(f'<h3 style="margin-top: 20px;">Challenge</h3><p style="color:#344054;font-size:.95rem">{block.get("question", block.get("task", ""))}</p>', unsafe_allow_html=True)
                if active not in completed_episodes:
                    with st.form(key=f"mcq_form_{story_id}_{active}_{i}"):
                        st.radio("", block["options"], label_visibility="collapsed", key=f"mcq_radio_{story_id}_{active}_{i}")
                        submitted = st.form_submit_button("Submit answer")
                    if submitted:
                        if st.session_state.get(f"mcq_radio_{story_id}_{active}_{i}") == block["answer"]:
                            if concept_id: advance_concept(concept_id, "APPLIED")
                            complete_current()
                        else:
                            st.error("Not quite. Try again.")
                    break
                else:
                    st.success(f"✓ You answered: {block['answer']}")
                    if "explanation" in block:
                        st.caption(block["explanation"])
            elif btype == "interactive":
                st.markdown(f'<h3 style="margin-top: 20px;">Challenge</h3><p style="color:#344054;font-size:.95rem">{block.get("task", "Interactive Lab")}</p>', unsafe_allow_html=True)
                if active not in completed_episodes:
                    from challenges import render_story_challenge
                    def _on_complete():
                        if concept_id: advance_concept(concept_id, "MASTERED")
                        complete_current()
                    render_story_challenge(story, lambda sid: _on_complete(), show_progress=False)
                    break
                else:
                    st.success("✓ Interactive lab complete.")
                    
        if active in completed_episodes:
            st.markdown(f'<div class="success-reveal" style="margin-top: 20px;"><b>✓ Episode {active:02d} complete</b></div>', unsafe_allow_html=True)
            if active < len(episodes) and st.button(f"Continue to Episode {active + 1:02d} →", key=f"continue_{story_id}_{active}"):
                st.session_state[f"active_level_{story_id}"] = active + 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        
    if context:
        with context:
            if st.button("Hide panel  ›", key=f"hide_context_button_{story_id}"):
                st.session_state[f"hide_context_{story_id}"] = True; st.rerun()
            context_panel(story)
    else:
        if st.button("‹ Show context", key=f"show_context_button_{story_id}"):
            st.session_state[f"hide_context_{story_id}"] = False; st.rerun()


def render_story_page(story_id):
    story = next(s for s in STORIES if s["id"] == story_id)
    level_list = LEVEL_CONTENT.get(story_id)
    if isinstance(level_list, dict) and level_list.get("format") == "episodic":
        return render_episodic_page(story_id, story, level_list)

    configure_page(f"{story['title']} · DBMS Story Lab")
    workspace_css()
    completed_levels = st.session_state.setdefault(f"completed_levels_{story_id}", set())
    active = st.session_state.setdefault(f"active_level_{story_id}", min(len(completed_levels) + 1, 8))
    progress = len(completed_levels)
    hide_context = st.session_state.get(f"hide_context_{story_id}", False)
    widths = [2.25, 6.1, 2.25] if not hide_context else [2.25, 8.35]
    columns = st.columns(widths)
    rail, main = columns[0], columns[1]
    context = columns[2] if not hide_context else None
    with rail:
        st.markdown(f'<div class="rail-title">{story["title"].upper()}</div><div class="rail-genre">{story["genre"]}</div><div class="rail-mission">{story["hook"]}</div><div class="rail-label">8 LEVELS</div>', unsafe_allow_html=True)
        available = list(range(1, min(progress + 2, 9)))
        selected = st.radio("Mission levels", available, index=max(0, min(active, len(available)) - 1), format_func=lambda n: f"{n:02d}  {LEVELS[n-1][0]}", label_visibility="collapsed", key=f"level_picker_{story_id}")
        if selected != active:
            st.session_state[f"active_level_{story_id}"] = selected; st.rerun()
        for number, (name, skill) in enumerate(LEVELS, 1):
            if number in available: continue
            st.markdown(f'<div class="level-static locked"><b>🔒 {number:02d} &nbsp; {name}</b>{skill}</div>', unsafe_allow_html=True)
    with main:
        st.markdown('<div class="workspace-main">', unsafe_allow_html=True)
        level_name, level_skill = LEVELS[active - 1]
        level_list = LEVEL_CONTENT.get(story_id) or [{}] * 8
        level_data = level_list[active - 1] if active <= len(level_list) else {}
        challenge_type = level_data.get("type", "interactive")

        st.markdown(
            f'<div class="workspace-eyebrow">LEVEL {active:02d} · {level_name.upper()} &nbsp;&nbsp; +{LEVEL_XP[active - 1]} XP</div>'
            f'<h1>{story["title"]}: {level_name}</h1>',
            unsafe_allow_html=True,
        )

        narrative = level_data.get("narrative", story["opening"])
        st.markdown(f'<div class="objective">{narrative}</div>', unsafe_allow_html=True)

        def complete_current(sid):
            levels = st.session_state.setdefault(f"completed_levels_{sid}", set())
            current = st.session_state.get(f"active_level_{sid}", 1)
            if current not in levels:
                levels.add(current)
                st.session_state.xp += LEVEL_XP[current - 1]
                if current == 8:
                    st.session_state.completed.add(sid)
            st.session_state[f"active_level_{sid}"] = min(current + 1, 8)
            save_progress()

        # ── Read level ─────────────────────────────────────────────────────────
        if challenge_type == "read":
            task_text = level_data.get("task", "")
            st.markdown(
                f'<p style="margin-top:1rem;color:#667085;font-size:.94rem">{task_text}</p>',
                unsafe_allow_html=True,
            )
            if active not in completed_levels:
                if st.button("✓ Understood — proceed", key=f"proceed_{story_id}_{active}"):
                    complete_current(story_id)
                    st.rerun()

        # ── MCQ level ──────────────────────────────────────────────────────────
        elif challenge_type == "mcq":
            task_text = level_data.get("task", "")
            st.markdown(
                f'<h3>Your question</h3>'
                f'<p style="margin:.5rem 0 1rem;color:#344054;font-size:.95rem">{task_text}</p>',
                unsafe_allow_html=True,
            )
            if active not in completed_levels:
                with st.form(key=f"mcq_form_{story_id}_{active}"):
                    st.radio(
                        "",
                        level_data.get("options", []),
                        label_visibility="collapsed",
                        key=f"mcq_radio_{story_id}_{active}",
                    )
                    submitted = st.form_submit_button("Submit answer")
                if submitted:
                    chosen = st.session_state.get(f"mcq_radio_{story_id}_{active}")
                    if chosen == level_data.get("answer"):
                        complete_current(story_id)
                        st.rerun()
                    else:
                        st.error(level_data.get("feedback_wrong", "Not quite. Try again."))

        # ── Interactive level (Final Boss) ──────────────────────────────────────
        else:
            task_text = level_data.get("task", "")
            st.markdown(
                f'<p style="margin-top:.5rem;color:#667085;font-size:.94rem">{task_text}</p>',
                unsafe_allow_html=True,
            )
            with st.expander("💡 Show hint"):
                st.markdown(
                    '<div class="hint-box">Start with the evidence that repeats. '
                    'Look for a pattern that connects the facts.</div>',
                    unsafe_allow_html=True,
                )
            with st.expander("Need another clue?"):
                st.write("The database is most useful when reasoning about related records as a set, not one at a time.")
            st.markdown('<h3>Interactive lab</h3>', unsafe_allow_html=True)
            render_story_challenge(story, complete_current, show_progress=False)

        # ── Success reveal ─────────────────────────────────────────────────────
        if active in completed_levels:
            if challenge_type == "mcq":
                reveal_text = level_data.get("feedback_correct", "Level complete.")
            elif challenge_type == "read":
                reveal_text = "Evidence logged. The investigation advances."
            else:
                reveal_text = f'What you discovered: <b>{story["primary"]}</b>.'
            st.markdown(
                f'<div class="success-reveal"><b>✓ Level {active:02d} — {level_name} complete</b>'
                f'<br>{reveal_text}</div>',
                unsafe_allow_html=True,
            )
            if active < 8 and st.button(f"Continue to Level {active + 1:02d} →", key=f"continue_{story_id}_{active}"):
                st.session_state[f"active_level_{story_id}"] = active + 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
    if context:
        with context:
            if st.button("Hide panel  ›", key=f"hide_context_button_{story_id}"):
                st.session_state[f"hide_context_{story_id}"] = True; st.rerun()
            context_panel(story)
    else:
        if st.button("‹ Show context", key=f"show_context_button_{story_id}"):
            st.session_state[f"hide_context_{story_id}"] = False; st.rerun()
