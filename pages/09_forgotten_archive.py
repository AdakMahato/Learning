import streamlit as st
from field_notebook import show_concept_card, recap_and_save
from ui import ensure_state, mark_complete, sidebar, configure_page

STORY_ID = 9
TOTAL_LEVELS = 8

def level_done(story_id: int, level: int) -> bool:
    return bool(st.session_state.get(f"mission_{story_id}_{level}"))

def cliffhanger(text: str):
    st.markdown(f"> *{text}*")

def level_1():
    st.subheader("Level 1 — Discovery")
    st.write(
        "You've been sent underground to catalogue a pre-collapse records "
        "office. Three departments kept their own paper trails: Payroll, "
        "Housing, and Rationing. You find the same names spelled slightly "
        "differently across all three."
    )
    show_concept_card("file_based_system", STORY_ID)
    st.image(
        "https://placehold.co/600x200?text=Three+separate+paper+archives",
        use_container_width=True,
    )
    if st.button("Keep exploring the archive →", key="l1_continue"):
        mark_complete(STORY_ID, amount=20, level=1, total_levels=TOTAL_LEVELS)
        cliffhanger("One name appears in all three folders — with three different addresses.")
        st.rerun()

def level_2():
    st.subheader("Level 2 — Investigation")
    st.write(
        "Same person, three addresses. You ask the site's old caretaker "
        "what went wrong."
    )
    show_concept_card("data_redundancy", STORY_ID)
    answer = st.radio(
        "What's actually causing the three different addresses?",
        [
            "The person moved three times and nobody noticed",
            "The same fact (address) is stored in three places with no link between them, so updates only ever hit one copy",
            "The archive is simply too old to trust",
        ],
        index=None,
        key="l2_answer",
    )
    if answer and st.button("Submit finding", key="l2_submit"):
        if answer.startswith("The same fact"):
            recap_and_save("data_redundancy", STORY_ID, 2)
            mark_complete(STORY_ID, amount=25, level=2, total_levels=TOTAL_LEVELS)
            cliffhanger("If one folder is updated and the others aren't... which one do you believe next?")
            st.rerun()
        else:
            st.warning("Look again — this happens even when nobody moved. Think about how many copies exist.")

THREE_SCHEMA_ITEMS = {
    "Front desk request form": "External",
    "Filing rulebook for the whole archive": "Conceptual",
    "Actual shelves and boxes": "Internal",
}

def level_3():
    st.subheader("Level 3 — Complexity")
    st.write(
        "The caretaker sketches how the archive is *supposed* to work — "
        "three layers, each hiding the one below it. Match each layer to "
        "what it represents."
    )
    show_concept_card("three_schema", STORY_ID)

    answers = {}
    cols = st.columns(3)
    layers = ["External", "Conceptual", "Internal"]
    items = list(THREE_SCHEMA_ITEMS.keys())
    for i, item in enumerate(items):
        with cols[i]:
            answers[item] = st.selectbox(item, ["-- choose --"] + layers, key=f"l3_{i}")

    if st.button("Lock in the mapping", key="l3_submit"):
        correct = all(answers[item] == THREE_SCHEMA_ITEMS[item] for item in items)
        if correct:
            recap_and_save("three_schema", STORY_ID, 3)
            mark_complete(STORY_ID, amount=30, level=3, total_levels=TOTAL_LEVELS)
            cliffhanger("The rulebook layer has a torn page — and it's the page defining Payroll's records.")
            st.rerun()
        else:
            st.warning("Not quite — remember: front desk sees the request, rulebook defines structure, shelves hold the physical boxes.")

def level_4():
    st.subheader("Level 4 — Failure")
    st.write(
        "The torn rulebook page meant Housing kept writing new addresses "
        "in a *different format* than Payroll. Before you look at what "
        "happened — predict it."
    )
    show_concept_card("data_independence", STORY_ID)

    prediction = st.radio(
        "If applications don't share one agreed structure, what breaks first?",
        [
            "Nothing — the data still exists somewhere",
            "Queries that assume one format silently miss or misread records in the other format",
            "The archive physically collapses",
        ],
        index=None,
        key="l4_predict",
    )

    if prediction:
        if st.button("Reveal what actually happened", key="l4_reveal"):
            st.session_state["l4_revealed"] = True

    if st.session_state.get("l4_revealed"):
        st.error(
            "Confirmed: Rationing's report silently dropped 40% of Housing's "
            "records because it expected 'Street, City' and got 'City, Street'. "
            "No error, no crash — just quietly wrong answers."
        )
        correct = prediction == (
            "Queries that assume one format silently miss or misread records in the other format"
        )
        if correct:
            st.success("Your prediction matched — that's exactly the failure mode.")
        else:
            st.info("Different from what you predicted — this is the dangerous kind of bug: no error message, just wrong results.")

        if st.button("Continue", key="l4_continue"):
            recap_and_save("data_independence", STORY_ID, 4)
            mark_complete(STORY_ID, amount=35, level=4, total_levels=TOTAL_LEVELS)
            cliffhanger("Now you need to find ONE record fast, in a room of ten thousand boxes.")
            st.rerun()

def level_5():
    st.subheader("Level 5 — Optimization")
    st.write(
        "You need record #8,842. Without any labels, that means checking "
        "boxes one by one."
    )
    show_concept_card("sequential_scan", STORY_ID)
    show_concept_card("index", STORY_ID)

    total_boxes = st.slider("How many boxes are in the room?", 100, 10000, 5000, key="l5_boxes")
    st.write(f"**Without a shelf directory:** up to {total_boxes} boxes checked (sequential scan).")
    st.write(f"**With a shelf directory (index):** roughly {max(1, total_boxes.bit_length())} steps to narrow it down.")

    if st.button("I see the difference — move on", key="l5_continue"):
        recap_and_save("index", STORY_ID, 5)
        mark_complete(STORY_ID, amount=30, level=5, total_levels=TOTAL_LEVELS)
        cliffhanger("You find record #8,842 — but its 'employee ID' contradicts the Payroll copy from Level 2.")
        st.rerun()

def level_6():
    st.subheader("Level 6 — Conflict")
    st.write(
        "Two boxes claim two different employee IDs for the same person. "
        "If this archive had been a real database from day one, which "
        "single rule would have stopped this?"
    )
    show_concept_card("constraints", STORY_ID)
    choice = st.radio(
        "Pick the rule",
        [
            "A stronger padlock on the archive door",
            "A PRIMARY KEY / UNIQUE constraint on employee ID, enforced by the system itself",
            "Hiring a second caretaker to double-check by hand",
        ],
        index=None,
        key="l6_choice",
    )
    if choice and st.button("Submit", key="l6_submit"):
        if "PRIMARY KEY" in choice:
            recap_and_save("constraints", STORY_ID, 6)
            mark_complete(STORY_ID, amount=35, level=6, total_levels=TOTAL_LEVELS)
            cliffhanger("A sudden collapse in the east wing — and the only copy of Level 4's fix is under the rubble.")
            st.rerun()
        else:
            st.warning("A human checking by hand is exactly what file-based systems relied on — and exactly what failed. What would the *system itself* enforce automatically?")

def level_7():
    st.subheader("Level 7 — Disaster")
    st.write(
        "The east wing collapsed mid-update. Some records are half-written. "
        "You have one working duplicate archive in another building, "
        "three weeks out of date."
    )
    show_concept_card("backup_recovery", STORY_ID)
    choice = st.radio(
        "What's your recovery move?",
        [
            "Trust the collapsed wing's half-written records — they're more recent",
            "Restore from the three-week-old duplicate and treat anything after as lost until reconstructed",
            "Guess based on which version 'looks' more complete",
        ],
        index=None,
        key="l7_choice",
    )
    if choice and st.button("Decide", key="l7_submit"):
        if choice.startswith("Restore from the three-week-old"):
            recap_and_save("backup_recovery", STORY_ID, 7)
            mark_complete(STORY_ID, amount=40, level=7, total_levels=TOTAL_LEVELS)
            cliffhanger("The archive survives — barely. One final question remains before you can close the case.")
            st.rerun()
        else:
            st.warning("Half-written records mid-crash are the least trustworthy thing in the building. A slightly old, complete backup beats a fresh, broken one.")

FINAL_QUIZ = [
    ("The root cause of the whole case was...", [
        "Bad luck",
        "No single system enforcing one shared, consistent structure across departments",
    ], 1),
    ("What would have caught the address format mismatch immediately?", [
        "Data independence — one shared logical structure all apps rely on",
        "A bigger archive room",
    ], 0),
    ("What made record #8,842 fast to find?", [
        "An index acting like a shelf directory",
        "Reading every box in order",
    ], 0),
]

def level_8():
    st.subheader("Level 8 — Final Boss: Close the Case")
    st.write("Explain the case to your supervisor. Get all three right to close it.")

    score = 0
    for i, (q, opts, correct_idx) in enumerate(FINAL_QUIZ):
        choice = st.radio(q, opts, index=None, key=f"l8_q{i}")
        if choice == opts[correct_idx]:
            score += 1

    if st.button("Submit final report", key="l8_submit"):
        if score == len(FINAL_QUIZ):
            mark_complete(STORY_ID, amount=100, level=8, total_levels=TOTAL_LEVELS)
            st.balloons()
            st.success(
                "**Case closed.** You've earned the DBMS Foundations badge — "
                "you now understand why file-based systems fail and what a "
                "real database engine actually buys you."
            )
        else:
            st.warning(f"{score}/{len(FINAL_QUIZ)} correct — review the earlier levels' Field Notebook cards and try again.")

LEVEL_RENDERERS = {
    1: level_1, 2: level_2, 3: level_3, 4: level_4,
    5: level_5, 6: level_6, 7: level_7, 8: level_8,
}

def render_story_page():
    configure_page("The Forgotten Archive · DBMS Story Lab")
    sidebar("story")
    ensure_state()
    st.markdown('<div class="eyebrow">INVESTIGATION 09</div><h1>🗄️ The Forgotten Archive</h1>', unsafe_allow_html=True)

    current_level = 1
    for lvl in range(1, TOTAL_LEVELS + 1):
        if level_done(STORY_ID, lvl):
            current_level = min(lvl + 1, TOTAL_LEVELS)
        else:
            current_level = lvl
            break
    if level_done(STORY_ID, TOTAL_LEVELS):
        current_level = TOTAL_LEVELS

    st.progress(sum(level_done(STORY_ID, l) for l in range(1, TOTAL_LEVELS + 1)) / TOTAL_LEVELS)
    LEVEL_RENDERERS[current_level]()

render_story_page()
