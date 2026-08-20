"""
field_notebook.py
------------------
A reusable "concept companion" layer for DBMS Story Lab.
"""

import streamlit as st

CONCEPTS = {
    "file_based_system": {
        "term": "File-Based System",
        "analogy": (
            "Imagine every department in a company keeps its own paper "
            "folders. Payroll has an 'Employees' folder, HR has its own "
            "'Employees' folder too — same people, two folders, and "
            "nobody tells the other side when something changes."
        ),
        "formal": (
            "Data stored directly in flat files by each application, "
            "with no shared engine managing consistency between them."
        ),
    },
    "data_redundancy": {
        "term": "Data Redundancy",
        "analogy": (
            "Two folders both say 'John's phone number' — but one was "
            "updated last month and the other wasn't. Now which one do "
            "you trust?"
        ),
        "formal": (
            "The same fact stored in multiple places, risking "
            "inconsistency when only one copy gets updated."
        ),
    },
    "data_independence": {
        "term": "Data Independence",
        "analogy": (
            "A good filing cabinet lets the archivist reorganise the "
            "shelves without the visitors upstairs ever noticing — they "
            "just ask the front desk and get their file either way."
        ),
        "formal": (
            "The ability to change how data is stored or structured "
            "without forcing every application that uses it to change too."
        ),
    },
    "three_schema": {
        "term": "Three-Schema Architecture",
        "analogy": (
            "Front desk (External) → the visitor's request form. "
            "Filing rulebook (Conceptual) → how the whole archive is "
            "organised. Actual shelves (Internal) → the physical boxes. "
            "Change the shelves, the rulebook and front desk stay the same."
        ),
        "formal": (
            "External / Conceptual / Internal levels that separate how "
            "users see data, how it's logically modeled, and how it's "
            "physically stored."
        ),
    },
    "constraints": {
        "term": "Integrity Constraints",
        "analogy": (
            "A house rule: 'no file leaves the archive without a "
            "signature.' It's not the archivist's memory enforcing this "
            "— it's a rule built into the front desk itself."
        ),
        "formal": (
            "Rules (primary key, foreign key, NOT NULL, etc.) enforced "
            "by the DBMS itself, not by application code remembering to check."
        ),
    },
    "sequential_scan": {
        "term": "Sequential (Full) Scan",
        "analogy": (
            "Looking for one letter by opening every single box in the "
            "archive, one at a time, floor to ceiling."
        ),
        "formal": (
            "Reading every row in a table to find matches, with cost "
            "proportional to table size."
        ),
    },
    "index": {
        "term": "Index",
        "analogy": (
            "A labelled drawer directory at the entrance: 'Boxes 1-50: "
            "Shelf A. Boxes 51-100: Shelf B.' You jump straight to the "
            "right shelf instead of checking every box."
        ),
        "formal": (
            "An auxiliary structure (commonly a B-tree) that lets the "
            "engine jump to matching rows instead of scanning the whole table."
        ),
    },
    "backup_recovery": {
        "term": "Backup & Recovery",
        "analogy": (
            "The archive keeps a duplicate copy in a separate building. "
            "If a fire destroys the shelves, the duplicate lets you "
            "rebuild instead of losing everything."
        ),
        "formal": (
            "Logging and backup mechanisms that let a DBMS restore "
            "correct data after a crash or failure."
        ),
    },
    "what_is_dbms": {
        "term": "Database Management System (DBMS)",
        "analogy": "A highly organized central archive where every department requests information through a dedicated, rule-following librarian.",
        "formal": "A software system designed to store, retrieve, and manage data safely and efficiently."
    },
    "tables_rows_cols": {
        "term": "Tables, Rows, and Columns",
        "analogy": "Database = filing room. Table = cabinet. Row = individual file. Column = a specific field on every file.",
        "formal": "Data is organized into tables (entities), where each row is a record (a specific instance), and each column is an attribute (a property)."
    },
    "primary_key": {
        "term": "Primary Key",
        "analogy": "Like a citizen's social security number, it identifies exactly one person uniquely.",
        "formal": "A unique identifier for each row in a table. Must be unique and cannot be NULL."
    },
    "relationships_fk": {
        "term": "Relationships & Foreign Keys",
        "analogy": "Instead of writing down the whole university address on your hospital form, you just write the university's official ID code.",
        "formal": "A foreign key is a column that creates a link between two tables, pointing to the primary key of another table."
    },
    "sql_basics": {
        "term": "Structured Query Language (SQL)",
        "analogy": "The standard language for communicating with relational databases.",
        "formal": "A declarative language used to query and modify data in a relational database system."
    },
    "transactions_acid": {
        "term": "ACID Transactions",
        "analogy": "A sequence of operations treated as a single, all-or-nothing logical unit of work. Like a bank transfer: both deduct and add must succeed together.",
        "formal": "Atomicity, Consistency, Isolation, Durability guarantee that database transactions are processed reliably."
    },
    "indexing": {
        "term": "Indexes",
        "analogy": "Like an index at the back of a book. Instead of reading every page to find 'Transactions', you jump straight to page 412.",
        "formal": "An auxiliary data structure (often a B-Tree) that improves data retrieval speed at the cost of slower writes and more storage."
    },
}

def _ensure_notebook_state():
    if "concept_mastery" not in st.session_state:
        st.session_state.concept_mastery = {}
    if "notebook_seen" not in st.session_state:
        st.session_state.notebook_seen = set()
    if "notebook_recaps" not in st.session_state:
        st.session_state.notebook_recaps = []

STAGES = ["UNKNOWN", "INTRODUCED", "VISUALIZED", "PRACTICED", "APPLIED", "MASTERED"]

def advance_concept(concept_id: str, stage: str):
    _ensure_notebook_state()
    current = st.session_state.concept_mastery.get(concept_id, "UNKNOWN")
    if STAGES.index(stage) > STAGES.index(current):
        st.session_state.concept_mastery[concept_id] = stage
        from persistence import save_progress
        save_progress()

def show_concept_card(concept_id: str, story_id: int):
    _ensure_notebook_state()
    concept = CONCEPTS.get(concept_id, {})
    if not concept: return
    
    first_time = concept_id not in st.session_state.notebook_seen
    st.session_state.notebook_seen.add(concept_id)
    advance_concept(concept_id, "INTRODUCED")

    with st.expander(f"📓 {concept.get('term', concept_id)}", expanded=first_time):
        st.markdown(concept.get("analogy", ""))
        st.caption(f"**In DBMS terms:** {concept.get('formal', '')}")
        if not first_time:
            st.caption("_(You've seen this before — quick refresher.)_")

def recap_and_save(concept_id: str, story_id: int, level: int):
    _ensure_notebook_state()
    concept = CONCEPTS.get(concept_id, {})
    if not concept: return
    advance_concept(concept_id, "MASTERED")
    st.success(f"✅ Concept unlocked: **{concept.get('term', concept_id)}**")
    
    # Avoid duplicate recaps
    if not any(r["term"] == concept.get("term", concept_id) for r in st.session_state.notebook_recaps):
        st.session_state.notebook_recaps.append(
            {
                "story_id": story_id,
                "level": level,
                "term": concept.get("term", concept_id),
                "formal": concept.get("formal", ""),
                "id": concept_id
            }
        )

def render_mastery_state(concept_id):
    current = st.session_state.concept_mastery.get(concept_id, "UNKNOWN")
    idx = STAGES.index(current)
    html = '<div style="font-size: 0.85rem; margin-top: 10px; color: #667085;">'
    for i, stage in enumerate(STAGES[1:]):
        mark = "✓" if i + 1 <= idx else "○"
        color = "#10B981" if i + 1 <= idx else "#D1D5DB"
        html += f'<span style="color: {color}; margin-right: 8px;">{mark} {stage.capitalize()}</span>'
    html += '</div>'
    return html

def render_glossary_page():
    from ui import configure_page, sidebar
    configure_page("Field Notebook · DBMS Story Lab")
    sidebar("notebook")
    _ensure_notebook_state()
    st.markdown('<div class="eyebrow">GLOSSARY</div><h1>📓 Field Notebook</h1><p class="muted">Every concept you\'ve unlocked so far, in your own investigation order.</p>', unsafe_allow_html=True)

    if not st.session_state.notebook_recaps:
        st.info("Nothing here yet — solve your first challenge to start filling this in.")
        return

    for entry in st.session_state.notebook_recaps:
        st.markdown(f"**{entry['term']}**  \n{entry['formal']}")
        st.caption(f"Unlocked in Story {entry['story_id']}, Level {entry['level']}")
        st.markdown(render_mastery_state(entry.get("id")), unsafe_allow_html=True)
        st.divider()
