import sqlite3
import re
import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def sql_db():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE people(id INTEGER PRIMARY KEY, name TEXT, city TEXT);
    CREATE TABLE sightings(id INTEGER PRIMARY KEY, person_id INTEGER, location TEXT, event_time TEXT);
    CREATE TABLE locations(id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE merchants(id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE goods(id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE transactions(id INTEGER PRIMARY KEY, merchant_id INTEGER, good_id INTEGER, amount REAL, year INTEGER);
    INSERT INTO people VALUES
      (1,'Mara','North'),(2,'Ivo','East'),(3,'Nia','North'),(4,'Sol','West');
    INSERT INTO sightings VALUES
      (1,1,'Gate-7','03:12'),(2,1,'Dock-2','03:14'),(3,2,'Gate-7','03:20'),
      (4,3,'Market','03:41'),(5,4,'Dock-2','03:52');
    INSERT INTO locations VALUES
      (1,'Gate-7'),(2,'Dock-2'),(3,'Market'),(4,'Archive');
    INSERT INTO merchants VALUES
      (1,'Aster'),(2,'Borin'),(3,'Cyra'),(4,'Dalen');
    INSERT INTO goods VALUES
      (1,'Grain'),(2,'Copper'),(3,'Salt');
    INSERT INTO transactions VALUES
      (1,1,1,500,101),(2,1,2,120,102),(3,2,1,900,102),
      (4,3,3,300,103),(5,2,2,700,103),(6,1,1,1100,104);
    """)
    con.commit()
    return con

def sql_challenge(story_id):
    st.markdown("### 🧪 Live SQL terminal")
    st.caption("This is a safe in-memory SQLite sandbox. Nothing is written to your machine.")
    con = sql_db()

    examples = {
        1: "SELECT p.name, s.location, s.event_time\nFROM people p JOIN sightings s ON p.id=s.person_id\nWHERE p.id=1;",
        6: "SELECT m.name, SUM(t.amount) AS total\nFROM merchants m JOIN transactions t ON m.id=t.merchant_id\nGROUP BY m.id, m.name\nORDER BY total DESC;",
    }
    default = examples.get(story_id, "SELECT * FROM people;")
    query = st.text_area("SQL", value=default, height=150, key=f"sql_{story_id}")
    result_key = f"sql_result_{story_id}"
    if st.button("▶ Execute", key=f"exec_{story_id}"):
        try:
            if not re.match(r"^\s*(SELECT|WITH|PRAGMA)\b", query, re.I):
                st.warning("For this challenge, use a read-only SELECT/CTE query.")
            else:
                df = pd.read_sql_query(query, con)
                st.session_state[result_key] = df.to_dict("records")
        except Exception as e:
            st.error(f"SQL error: {e}")
    if result_key in st.session_state:
        result = pd.DataFrame(st.session_state[result_key])
        st.markdown("#### Query results")
        st.success(f"Rows returned: {len(result)} · SQLite sandbox")
        st.dataframe(result, use_container_width=True, hide_index=True)
        if story_id in (1, 6) and len(result) > 0:
            st.info("The query found usable evidence. Submit this result to resolve the current investigation.")
            if st.button("✓ Submit answer", key=f"submit_sql_{story_id}"):
                return True
    with st.expander("Available tables"):
        st.code("people(id, name, city)\nsightings(id, person_id, location, event_time)\nlocations(id, name)\nmerchants(id, name)\ngoods(id, name)\ntransactions(id, merchant_id, good_id, amount, year)")
    return False

def normalization_challenge():
    st.markdown("### 🧬 Schema surgery")
    st.write("The implant stores a person's name and city in multiple rows. Which design removes the update anomaly?")
    options = {
        "A": "Keep person_id, person_name, city in every event row.",
        "B": "Create people(person_id, person_name, city) and reference person_id from events.",
        "C": "Store the person's name only in a free-text event description.",
        "D": "Duplicate the people table once per department.",
    }
    choice = st.radio("Choose the redesign", list(options.keys()),
                      format_func=lambda x: f"{x}. {options[x]}",
                      key="norm_choice")
    if st.button("Validate schema", key="norm_validate"):
        if choice == "B":
            st.success("Correct. The repeated fact is stored once and referenced by key.")
            return True
        st.error("Not quite. Look for the functional dependency person_id → person_name, city.")
    return False

def fill_gap_challenge():
    st.markdown("### 🧩 Fill the missing pieces")
    st.write("Complete the SQL statement that finds zones with more than one active route.")
    c1, c2, c3 = st.columns(3)
    with c1:
        group = st.selectbox("Blank 1", ["WHERE", "GROUP BY", "ORDER BY"], key="fg1")
    with c2:
        count = st.selectbox("Blank 2", ["COUNT(DISTINCT active_route_id)", "SUM(active_route_id)", "MAX(zone_id)"], key="fg2")
    with c3:
        having = st.selectbox("Blank 3", ["HAVING", "WHERE", "LIMIT"], key="fg3")
    if st.button("Check gaps", key="fgcheck"):
        if group == "GROUP BY" and count == "COUNT(DISTINCT active_route_id)" and having == "HAVING":
            st.success("Perfect. GROUP BY → COUNT(DISTINCT ...) → HAVING captures the contradiction.")
            return True
        st.error("One or more blanks are wrong.")
    return False

def index_visualizer():
    st.markdown("### 🌲 Index scan visualizer")
    n = st.slider("Rows in table", 50, 1000, 300, 50, key="idx_n")
    indexed = st.checkbox("Create B-tree index on event_time", value=False, key="idx_on")
    target = st.slider("Rows matching time range", 1, max(2, n // 2), min(10, n // 2), key="idx_target")
    scan_cost = n
    index_cost = max(4, int(n ** 0.5)) + target if indexed else n
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Sequential scan", "Index strategy"], y=[scan_cost, index_cost]))
    fig.update_layout(
        paper_bgcolor="#101322", plot_bgcolor="#101322",
        font_color="#dfe3f2", height=320,
        yaxis_title="Approximate work units"
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    if indexed and index_cost < scan_cost:
        st.success("The range predicate can avoid visiting most table rows.")
        return True
    st.info("Try enabling the index and keep the matching range selective.")
    return False

def transaction_simulator():
    st.markdown("### 🔐 Transaction / locking simulator")
    st.write("Two agents attempt to reserve the same crate. Choose the concurrency policy.")
    policy = st.selectbox("Policy", [
        "No transaction",
        "Read Committed",
        "Serializable + row lock",
        "Snapshot / MVCC"
    ], key="tx_policy")
    if st.button("Simulate race", key="tx_sim"):
        if policy == "Serializable + row lock":
            st.success("Agent A locks the crate → commits → Agent B observes the updated state. Lost update prevented.")
            return True
        if policy == "Snapshot / MVCC":
            st.success("Consistent reads are preserved, but write conflicts must still be handled correctly.")
            return True
        if policy == "Read Committed":
            st.warning("Dirty reads are prevented, but this alone does not serialize all conflicting updates.")
        else:
            st.error("Race condition: both agents can observe the same old quantity and overwrite one another.")
    return False

def distributed_decision():
    st.markdown("### 🚀 Blackout decision simulator")
    st.write("Communications are down for six hours. A colony must continue allocating cargo.")
    consistency = st.radio("Choose your priority", [
        "Strict consistency — refuse uncertain allocations",
        "Availability — allocate locally and reconcile later"
    ], key="dist_choice")
    rule = st.selectbox("Conflict rule", [
        "Last writer wins",
        "Quantity reconciliation",
        "Manual review for conflicts"
    ], key="dist_rule")
    if st.button("Commit architecture", key="dist_commit"):
        if consistency.startswith("Availability") and rule == "Quantity reconciliation":
            st.success("Good trade-off. Local availability is preserved and quantity conflicts have an explicit reconciliation rule.")
            return True
        if consistency.startswith("Strict"):
            st.info("This preserves consistency, but unavailable peers can make the station unable to allocate.")
        else:
            st.warning("Availability without a robust reconciliation policy risks silent over-allocation.")
    return False

def replication_visualizer():
    st.markdown("### 🤖 Replica consensus simulator")
    sectors = st.slider("Number of sectors", 3, 12, 7, key="replicas")
    quorum = sectors // 2 + 1
    votes = st.slider("Votes for proposed rule", 0, sectors, quorum, key="votes")
    fig = go.Figure()
    labels = ["Votes received", "Quorum required"]
    vals = [votes, quorum]
    fig.add_trace(go.Bar(x=labels, y=vals))
    fig.update_layout(
        paper_bgcolor="#101322", plot_bgcolor="#101322",
        font_color="#dfe3f2", height=300,
        yaxis_title="Sectors"
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    if votes >= quorum:
        st.success(f"Quorum reached: {votes}/{sectors}. The rule can be considered committed.")
        return True
    st.warning(f"Quorum not reached: {votes}/{sectors}. Keep the rule uncommitted.")
    return False

def mvcc_timeline():
    st.markdown("### 🕐 MVCC timeline")
    base = pd.DataFrame([
        ["T1", 1, "Report v1", "Read"],
        ["T2", 2, "Report v2", "Write + Commit"],
        ["T1", 3, "Report v1", "Read again"],
        ["T3", 4, "Report v2", "Read"],
    ], columns=["Transaction", "Time", "Version", "Operation"])
    st.dataframe(base, use_container_width=True, hide_index=True)
    isolation = st.selectbox("Isolation behavior", ["Read Committed", "Snapshot / MVCC"], key="mvcc_iso")
    if st.button("Replay timeline", key="mvcc_replay"):
        if isolation == "Snapshot / MVCC":
            st.success("T1 keeps its consistent snapshot: its second read can still see v1.")
            return True
        st.warning("Under Read Committed, a later statement may see the newly committed v2.")
    return False

def architecture_puzzle():
    st.markdown("### 🏛️ Three-schema architecture")
    st.write("Match each layer to its responsibility.")
    pairs = {
        "External": st.selectbox("External schema", ["User/application views", "Global logical structure", "Physical storage"], key="arch_ext"),
        "Conceptual": st.selectbox("Conceptual schema", ["Physical storage", "Global logical structure", "User/application views"], key="arch_con"),
        "Internal": st.selectbox("Internal schema", ["User/application views", "Global logical structure", "Physical storage"], key="arch_int"),
    }
    if st.button("Check architecture", key="arch_check"):
        if pairs == {
            "External": "User/application views",
            "Conceptual": "Global logical structure",
            "Internal": "Physical storage",
        }:
            st.success("Correct. This separation is the foundation for data independence.")
            return True
        st.error("Think from the user's view → logical organization → physical storage.")
    return False

def er_algebra_puzzle():
    st.markdown("### 🏗️ ER → relational algebra")
    st.write("A city has many buildings. Each building belongs to one district. Find buildings in district 'North'.")
    operation = st.selectbox("Choose the relational algebra operation", [
        "Projection",
        "Selection",
        "Cartesian product",
        "Difference"
    ], key="ra_op")
    if st.button("Solve operation", key="ra_check"):
        if operation == "Selection":
            st.success("Correct. Selection filters tuples based on a predicate: σ(district='North')(Building).")
            return True
        st.error("The task filters rows, so choose the operation that selects tuples.")
    return False

def normalization_5nf():
    st.markdown("### 📜 Dependency ladder")
    st.write("Place the forms in the correct progression.")
    forms = st.multiselect("Select in order", ["1NF", "2NF", "3NF", "BCNF", "4NF", "5NF"], key="forms")
    if st.button("Validate ladder", key="ladder"):
        if forms == ["1NF", "2NF", "3NF", "BCNF", "4NF", "5NF"]:
            st.success("Full normalization ladder unlocked.")
            return True
        st.error("The canonical sequence is 1NF → 2NF → 3NF → BCNF → 4NF → 5NF.")
    return False

def render_story_challenge(story, mark_complete, show_progress=True):
    sid = story["id"]
    st.divider()

    challenge = None
    if sid in (1, 6):
        challenge = sql_challenge(sid)
    elif sid == 2:
        challenge = distributed_decision()
    elif sid == 3:
        challenge = index_visualizer()
    elif sid == 4:
        challenge = normalization_challenge()
    elif sid == 5:
        challenge = transaction_simulator()
    elif sid == 7:
        challenge = replication_visualizer()
    elif sid == 8:
        challenge = mvcc_timeline()
    elif sid == 9:
        challenge = architecture_puzzle()
    elif sid == 10:
        challenge = er_algebra_puzzle()
    elif sid == 11:
        challenge = normalization_5nf()

    if challenge:
        mark_complete(sid)

    if show_progress:
        st.markdown("### 🎯 Story progression")
        levels = [
            "Discovery", "Investigation", "Complexity", "Failure",
            "Optimization", "Conflict", "Disaster", "Scale / Final Boss"
        ]
        for i, level in enumerate(levels, 1):
            st.markdown(f"**Level {i} — {level}**")
        st.caption("The production version can turn each level into a separate route, unlock, score and persistence record.")
