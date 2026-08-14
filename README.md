# DBMS Story Lab — Streamlit

An interactive DBMS learning platform where database concepts are hidden inside 11 story-driven investigations.

## Included

### 11 storylines

1. The Vanishing Hour — SQL + modeling
2. Convoy Zero — distributed consistency
3. The Silence Between Signals — indexing/query plans
4. The Man Who Remembered Too Much — normalization
5. The Last Broadcast — transactions/concurrency
6. The Depth Ledger — advanced SQL
7. The Colony That Forgot Its Laws — replication/consensus
8. The Machine That Lied — MVCC/isolation
9. The Forgotten Archive — DBMS foundations
10. The Blueprint That Couldn't Exist — ER + relational theory
11. The Impossible Contract — 1NF–5NF + SQL

## Interactive modes

Each story has a different interaction style:

- SQL terminal
- Decision simulator
- Index visualization
- Schema surgery
- Transaction/locking simulator
- SQL investigation
- Replica/quorum visualization
- MVCC timeline
- Three-schema architecture puzzle
- Relational algebra puzzle
- Normalization fill/ordering challenge

## Run locally

```bash
cd dbms_story_lab
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Important

The SQL terminal uses an in-memory SQLite database. It is intentionally read-only for the demo challenge.

## Suggested next production upgrades

1. Make each of the 8 levels a real route rather than a single challenge.
2. Add persistent user profiles and XP.
3. Add a question/challenge database in JSON or SQLite.
4. Add SQL answer validation against expected result sets.
5. Add animated B+ tree, hash table, buffer pool and join visualizers.
6. Add ER diagram drawing with draggable entities.
7. Add transaction timeline playback.
8. Add save/resume.
9. Add badges and a final DBMS certification path.
10. Connect the 11 stories into one global progression map.
