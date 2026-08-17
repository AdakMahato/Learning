"""
level_content.py
----------------
Per-story, per-level narrative content and challenge definitions.
11 stories × 8 levels = 88 entries.

Each entry is a dict with:
  type        – "read" | "mcq" | "interactive"
  narrative   – story beat shown in the objective block
  task        – what the learner must do
  options     – (mcq only) list of answer strings
  answer      – (mcq only) the correct option string
  feedback_correct – (mcq only) explanation shown on correct answer
  feedback_wrong   – (mcq only) hint shown on wrong answer
"""

LEVEL_CONTENT = {
    # ──────────────────────────────────────────────────────────────────────────
    # 1 — The Vanishing Hour   (SQL + Modeling)
    # ──────────────────────────────────────────────────────────────────────────
    1: [
        {
            "type": "read",
            "narrative": (
                "It is 3:01 AM in Veridian. The city grid reports 3:00 AM as the last reliable "
                "timestamp — but residents are waking with conflicting memories of the hour that "
                "just passed. Three independent logging systems recorded different events at "
                "03:12, 03:14, and 03:41. Your terminal is the only system still holding fragments."
            ),
            "task": "Read the evidence. When you are ready, proceed to the investigation.",
        },
        {
            "type": "mcq",
            "narrative": (
                "The logs contain IDs that repeat across systems. Some sightings reference a "
                "person_id that doesn't appear in the people table at all. This breaks the link "
                "between events and the person who caused them."
            ),
            "task": "What constraint prevents a child table from referencing a non-existent parent row?",
            "options": [
                "A primary key constraint",
                "A foreign key constraint",
                "A unique constraint",
                "A NOT NULL constraint",
            ],
            "answer": "A foreign key constraint",
            "feedback_correct": (
                "Correct. A foreign key enforces referential integrity — the sighting's person_id "
                "must match an existing id in the people table."
            ),
            "feedback_wrong": (
                "Not quite. A foreign key ensures that a column's value in one table matches a "
                "value in another table's primary key, preventing orphaned references."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "You have a sightings table and a people table. You need each sighting alongside "
                "the person's name and city — but neither table alone has all the data."
            ),
            "task": "Which SQL operation combines columns from two related tables?",
            "options": ["UNION", "JOIN", "GROUP BY", "HAVING"],
            "answer": "JOIN",
            "feedback_correct": (
                "Correct. A JOIN combines rows from two tables based on a matching condition "
                "such as person_id — linking sightings with their corresponding person records."
            ),
            "feedback_wrong": (
                "Not quite. UNION stacks rows vertically. GROUP BY aggregates. "
                "JOIN is the operation that links two tables horizontally on a shared key."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Multiple systems wrote person_name and city alongside every event row. "
                "When Mara moved cities, 47 event records were updated — but 3 were missed. "
                "The city field now contradicts itself across the table."
            ),
            "task": "What type of anomaly causes a fact to become inconsistent when stored in multiple rows?",
            "options": [
                "Insertion anomaly",
                "Deletion anomaly",
                "Update anomaly",
                "Projection anomaly",
            ],
            "answer": "Update anomaly",
            "feedback_correct": (
                "Correct. An update anomaly occurs when the same fact appears in multiple rows "
                "and one update is missed, leaving contradictory data in the table."
            ),
            "feedback_wrong": (
                "Not quite. An update anomaly is when updating one row leaves other rows with "
                "the old (contradictory) value for the same real-world fact."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The system must scan 1.2 million event rows to find sightings at Gate-7 "
                "between 03:00 and 03:59. It checks every single row, even though less than "
                "0.1% will match the predicate."
            ),
            "task": "What database structure lets the query skip directly to relevant rows without scanning the entire table?",
            "options": ["A view", "An index", "A trigger", "A schema"],
            "answer": "An index",
            "feedback_correct": (
                "Correct. An index (typically a B-tree) allows the engine to locate matching "
                "rows in O(log n) time instead of scanning all rows sequentially."
            ),
            "feedback_wrong": (
                "Not quite. An index is a separate data structure that maps key values to row "
                "locations, dramatically reducing the number of rows the engine must read."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "During the blackout, three systems wrote partial updates. When power restored, "
                "some records showed a half-completed state — a person was checked in but "
                "never assigned a location."
            ),
            "task": "Which ACID property guarantees that a set of operations either all succeed or all have no effect?",
            "options": ["Atomicity", "Consistency", "Isolation", "Durability"],
            "answer": "Atomicity",
            "feedback_correct": (
                "Correct. Atomicity means a transaction is all-or-nothing — it never leaves "
                "the database in a partial state."
            ),
            "feedback_wrong": (
                "Not quite. Atomicity treats a group of operations as a single indivisible unit "
                "— either all complete or none of them do."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After the blackout, the system crashed mid-transaction. On restart, the DBMS "
                "must restore the database to a consistent state using the transaction log."
            ),
            "task": "What process restores a database to a consistent state after a crash?",
            "options": [
                "Normalization",
                "Partitioning",
                "Crash recovery",
                "Replication",
            ],
            "answer": "Crash recovery",
            "feedback_correct": (
                "Correct. Crash recovery uses the write-ahead log to redo committed transactions "
                "and undo incomplete ones after a system failure."
            ),
            "feedback_wrong": (
                "Not quite. Recovery uses a transaction log (write-ahead log) to replay or "
                "roll back operations that were in flight when the system crashed."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "You have access to the Veridian terminal. The evidence is fragmented across "
                "three tables. Reconstruct the timeline of the vanishing hour using your own SQL."
            ),
            "task": (
                "Use the SQL terminal to find all people sighted at Gate-7 or Dock-2 during "
                "the lost hour. Submit your result to close the case."
            ),
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 2 — Convoy Zero   (Distributed consistency)
    # ──────────────────────────────────────────────────────────────────────────
    2: [
        {
            "type": "read",
            "narrative": (
                "Three colonies — Veridian-A, B, and C — share a single cargo ledger. "
                "A 22-minute light-lag separates them. A blackout severed communication 6 hours ago. "
                "Colony A allocated Crate 7700 to a medical convoy. Colony C allocated the same "
                "crate to a fuel shipment 4 minutes later. Both believe they acted correctly."
            ),
            "task": "Read the incident briefing. Proceed to the consistency analysis.",
        },
        {
            "type": "mcq",
            "narrative": (
                "The cargo ledger is a database. Each colony holds its own copy. Changes must "
                "somehow propagate across a 22-minute light delay — a classic distributed systems problem."
            ),
            "task": "Which ACID property guarantees that once a transaction is committed, it survives crashes?",
            "options": ["Atomicity", "Consistency", "Isolation", "Durability"],
            "answer": "Durability",
            "feedback_correct": (
                "Correct. Durability means committed data is written to persistent storage "
                "and survives system failures — even a crash immediately after commit."
            ),
            "feedback_wrong": (
                "Not quite. Durability is the D in ACID — once the database says 'committed', "
                "the data must persist through crashes."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Both colonies committed locally. Neither had stale data when they wrote. "
                "Yet the combined ledger is now inconsistent — a fundamental distributed systems tension."
            ),
            "task": "Which theorem states a distributed system cannot simultaneously guarantee Consistency, Availability, and Partition tolerance?",
            "options": [
                "The ACID theorem",
                "The CAP theorem",
                "The BASE theorem",
                "Amdahl's Law",
            ],
            "answer": "The CAP theorem",
            "feedback_correct": (
                "Correct. The CAP theorem (Brewer, 2000) states that a distributed system can "
                "provide at most two of: Consistency, Availability, Partition tolerance."
            ),
            "feedback_wrong": (
                "Not quite. The CAP theorem is the fundamental trade-off in distributed "
                "database design — you must sacrifice one of the three guarantees."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "During the blackout, Colony C had no way to know Colony A had already committed. "
                "Without coordination, both committed conflicting writes to the same record."
            ),
            "task": "What is it called when two concurrent transactions both modify the same record and one silently overwrites the other?",
            "options": ["Dirty read", "Phantom read", "Lost update", "Non-repeatable read"],
            "answer": "Lost update",
            "feedback_correct": (
                "Correct. A lost update occurs when two transactions both read a value, compute "
                "a new value, and one write destroys the other's result."
            ),
            "feedback_wrong": (
                "Not quite. A lost update: T1 and T2 both read the same cargo quantity, "
                "both allocate from it, and T2's write makes T1's commit disappear."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After the blackout, the colonies can communicate again but hold different "
                "committed states for Crate 7700. The system must decide how to reconcile them."
            ),
            "task": "A model that allows nodes to diverge during partitions but guarantees eventual agreement is called what?",
            "options": [
                "Strong consistency",
                "Causal consistency",
                "Eventual consistency",
                "Linearizability",
            ],
            "answer": "Eventual consistency",
            "feedback_correct": (
                "Correct. Eventual consistency allows temporary divergence but guarantees all "
                "nodes will converge to the same state if no new updates arrive."
            ),
            "feedback_wrong": (
                "Not quite. Eventual consistency is used by DynamoDB, Cassandra, and many "
                "distributed systems — diverge now, converge later."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "One reconciliation rule: whichever allocation was committed earliest by global "
                "timestamp wins. The other is marked as a conflict and rolled back."
            ),
            "task": "What conflict resolution strategy gives priority to the earliest committed transaction?",
            "options": [
                "Last-writer-wins",
                "First-writer-wins",
                "Quorum voting",
                "Manual review",
            ],
            "answer": "First-writer-wins",
            "feedback_correct": (
                "Correct. First-writer-wins uses the earliest commit timestamp to determine "
                "the authoritative version."
            ),
            "feedback_wrong": (
                "Not quite. Last-writer-wins is the opposite. First-writer-wins privileges "
                "the transaction with the earliest commit timestamp."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The engineering team proposes requiring 2 of 3 colonies to confirm every "
                "allocation before it commits. During a blackout with only 1 reachable, "
                "no allocation can proceed."
            ),
            "task": "Refusing writes during a partition to preserve consistency reflects which side of the CAP theorem?",
            "options": [
                "Choosing Availability over Consistency",
                "Choosing Consistency over Availability",
                "Choosing Partition tolerance over both",
                "Choosing Durability over Isolation",
            ],
            "answer": "Choosing Consistency over Availability",
            "feedback_correct": (
                "Correct. Requiring quorum sacrifices availability (writes blocked during "
                "partitions) in exchange for consistency (no conflicting commits)."
            ),
            "feedback_wrong": (
                "Not quite. Quorum writes prioritise consistency — the system refuses to "
                "commit if it can't confirm a majority, accepting unavailability during partitions."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "Communications are down. Colony C is requesting immediate cargo allocation. "
                "You must decide the architecture: strict consistency or local availability "
                "with reconciliation."
            ),
            "task": (
                "Use the decision simulator to choose the right CAP trade-off and conflict "
                "resolution rule for the convoy crisis."
            ),
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 3 — The Silence Between Signals   (Indexing + Query plans)
    # ──────────────────────────────────────────────────────────────────────────
    3: [
        {
            "type": "read",
            "narrative": (
                "The Aurelia Array has collected 547 million radio burst records over 12 years. "
                "Analysts believe a non-random repeating signal is buried in the noise. "
                "The query to find repeating patterns takes 18 seconds. "
                "Analysts are giving up before the results arrive."
            ),
            "task": "Read the briefing. Proceed to begin the performance investigation.",
        },
        {
            "type": "mcq",
            "narrative": (
                "The current query reads every row in the 547-million-row table, computes a "
                "frequency match, and discards 99.98% of results. "
                "The planner confirms: cost = 547,000 sequential blocks."
            ),
            "task": "What type of scan reads every row in the table from start to finish?",
            "options": [
                "Index scan",
                "Bitmap scan",
                "Sequential scan (full table scan)",
                "Index-only scan",
            ],
            "answer": "Sequential scan (full table scan)",
            "feedback_correct": (
                "Correct. A sequential scan reads all blocks of the table in order, regardless "
                "of how many rows will match the predicate."
            ),
            "feedback_wrong": (
                "Not quite. A sequential scan processes every row — expensive when very few "
                "rows match, but sometimes optimal when most rows do."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "You propose creating an index on event_time. The planner now estimates it can "
                "skip to the relevant time range and read only 1,200 rows instead of 547 million."
            ),
            "task": "What internal data structure does a standard B-tree index use?",
            "options": [
                "A hash table",
                "A linked list",
                "A balanced tree of sorted key-value pairs",
                "A bitmap",
            ],
            "answer": "A balanced tree of sorted key-value pairs",
            "feedback_correct": (
                "Correct. A B-tree index is a self-balancing tree where internal nodes guide "
                "the search and leaf nodes store (key, row-pointer) pairs in sorted order."
            ),
            "feedback_wrong": (
                "Not quite. A B-tree keeps keys sorted so that range predicates (BETWEEN, >, <) "
                "traverse a narrow path rather than the entire dataset."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After adding the time index, analysts add a second filter: frequency_band = 'L'. "
                "The planner uses the time index but still scans half the retrieved rows for "
                "frequency_band without an index."
            ),
            "task": "What type of index covers two or more columns so both predicates can be evaluated at the index level?",
            "options": [
                "Partial index",
                "Clustered index",
                "Composite index",
                "Covering index (single column)",
            ],
            "answer": "Composite index",
            "feedback_correct": (
                "Correct. A composite (multi-column) index on (event_time, frequency_band) lets "
                "the engine apply both predicates at the index level, avoiding a second filter pass."
            ),
            "feedback_wrong": (
                "Not quite. A composite index stores multiple columns in a single index structure, "
                "making it efficient for queries that filter on all indexed columns together."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Despite the composite index, analysts run the pattern-aggregation query hourly "
                "and it still takes 3 seconds. The result changes only once every 6 hours "
                "but is computed from scratch each time."
            ),
            "task": "What database object stores the pre-computed result of a query and refreshes it on demand?",
            "options": [
                "A view",
                "A trigger",
                "A materialized view",
                "A stored procedure",
            ],
            "answer": "A materialized view",
            "feedback_correct": (
                "Correct. A materialized view physically stores the query result. When queried, "
                "the engine reads the cached result instead of re-executing the full aggregation."
            ),
            "feedback_wrong": (
                "Not quite. A regular view re-executes its query every time. "
                "A materialized view caches the result on disk and refreshes periodically."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The array runs real-time burst ingestion — thousands of rows per second — "
                "alongside analytical queries. They compete for I/O and locking resources."
            ),
            "task": "What architectural separation isolates high-volume transactional writes from complex analytical reads?",
            "options": [
                "Normalization",
                "Partitioning by date",
                "OLTP / OLAP separation",
                "Replication",
            ],
            "answer": "OLTP / OLAP separation",
            "feedback_correct": (
                "Correct. OLTP handles high-throughput row-level operations; OLAP handles "
                "complex aggregations over large datasets. Separating them prevents contention."
            ),
            "feedback_wrong": (
                "Not quite. OLTP/OLAP separation ensures write-heavy transactional and "
                "read-heavy analytical workloads don't interfere with each other."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The query planner shows two options: use the composite index (cost: 820) or "
                "a sequential scan with parallel workers (cost: 600). It chooses the sequential scan."
            ),
            "task": "In what situation does the planner correctly prefer a sequential scan over an existing index?",
            "options": [
                "When the table has fewer than 100 rows",
                "When the query returns a large fraction of the table's rows",
                "When the index is on a text column",
                "When the table has no primary key",
            ],
            "answer": "When the query returns a large fraction of the table's rows",
            "feedback_correct": (
                "Correct. When selectivity is low (many rows match), the overhead of random I/O "
                "through an index exceeds the cost of a single sequential pass."
            ),
            "feedback_wrong": (
                "Not quite. An index is beneficial only when highly selective. If 40% of the "
                "table matches, sequential scanning is often faster than random index I/O."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "You have a direct view into the Aurelia Array query planner. Adjust the table "
                "size, enable or disable the B-tree index, and change selectivity to observe "
                "exactly when the planner switches strategies."
            ),
            "task": "Use the index visualizer to find the configuration where the index strategy outperforms the sequential scan.",
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 4 — The Man Who Remembered Too Much   (Normalization)
    # ──────────────────────────────────────────────────────────────────────────
    4: [
        {
            "type": "read",
            "narrative": (
                "Elias Voss submitted his neural implant for diagnostic review. "
                "The archive returns 2 marriages, 2 employers, and 2 sets of childhood memories "
                "— each flagged as authentic. The implant stores life-events in a single flat table: "
                "event_id, event_type, person_name, person_city, event_detail. "
                "Every time Elias moved or changed jobs, someone added a new row. "
                "Old rows were never removed. The contradictions multiplied silently."
            ),
            "task": "Read the diagnostic report. Proceed to the schema analysis.",
        },
        {
            "type": "mcq",
            "narrative": (
                "The implant schema stores person_name and person_city in every event row. "
                "Elias's city appears in 312 rows: 309 say 'New Meridian', 3 say 'Old Meridian' "
                "— the city he left 14 years ago."
            ),
            "task": "What is a functional dependency?",
            "options": [
                "When two tables share a common column",
                "When the value of one attribute uniquely determines the value of another",
                "When a column cannot be NULL",
                "When two rows have the same primary key",
            ],
            "answer": "When the value of one attribute uniquely determines the value of another",
            "feedback_correct": (
                "Correct. A functional dependency X → Y means: knowing X's value tells you "
                "Y's value with certainty. Here, person_id → person_name, city."
            ),
            "feedback_wrong": (
                "Not quite. A functional dependency X → Y means: for any two tuples with the "
                "same X value, they must have the same Y value."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The events table contains a multi-valued tags column: 'family;work;education'. "
                "Querying for all 'work' events requires LIKE '%work%' — which cannot use an index."
            ),
            "task": "Which normal form requires that every column contain only atomic (indivisible) values?",
            "options": ["BCNF", "2NF", "3NF", "1NF"],
            "answer": "1NF",
            "feedback_correct": (
                "Correct. First Normal Form (1NF) requires atomic values — each cell holds "
                "one value, not a comma-separated list or nested set."
            ),
            "feedback_wrong": (
                "Not quite. 1NF is the foundation: no repeating groups, no multi-valued "
                "attributes, every column holds a single atomic value."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The composite primary key is (person_id, event_id). The column person_name "
                "depends only on person_id — not on the full composite key. "
                "This causes the city anomaly."
            ),
            "task": "What normal form requires every non-key attribute to be fully dependent on the ENTIRE primary key?",
            "options": ["1NF", "2NF", "3NF", "BCNF"],
            "answer": "2NF",
            "feedback_correct": (
                "Correct. 2NF eliminates partial dependencies — every non-key attribute must "
                "depend on the whole key, not a subset of a composite key."
            ),
            "feedback_wrong": (
                "Not quite. 2NF applies to tables with composite keys. It requires that no "
                "non-key column depends on just part of the composite primary key."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After 2NF, you split out a people table: (person_id, person_name, employer_id, "
                "employer_city). Now employer_city depends on employer_id — not on person_id. "
                "The dependency is transitive."
            ),
            "task": "What normal form eliminates transitive dependencies — where a non-key column depends on another non-key column?",
            "options": ["1NF", "2NF", "3NF", "4NF"],
            "answer": "3NF",
            "feedback_correct": (
                "Correct. 3NF requires that every non-key attribute depend directly on the "
                "primary key, not via a transitive chain through another non-key attribute."
            ),
            "feedback_wrong": (
                "Not quite. 3NF says: non-key attributes must not depend on other non-key "
                "attributes. Employer_city depends on employer_id, not person_id — transitive."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After 3NF, a remaining anomaly: employer_id → employer_city exists, but "
                "employer_id is not a candidate key in its table. BCNF is stricter than 3NF."
            ),
            "task": "What does BCNF (Boyce-Codd Normal Form) require that 3NF does not?",
            "options": [
                "No multi-valued attributes",
                "Every determinant must be a superkey",
                "No partial dependencies on composite keys",
                "No transitive dependencies between non-key columns",
            ],
            "answer": "Every determinant must be a superkey",
            "feedback_correct": (
                "Correct. BCNF strengthens 3NF: for every non-trivial functional dependency "
                "X → Y, X must be a superkey."
            ),
            "feedback_wrong": (
                "Not quite. BCNF says: every left-hand side of a non-trivial FD must be a "
                "superkey. 3NF allows some exceptions; BCNF does not."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After normalizing to BCNF, the memory search must JOIN 6 tables to reconstruct "
                "one event record. The planner estimates 14ms per lookup. "
                "The implant's real-time interface needs sub-millisecond recall."
            ),
            "task": "What technique intentionally introduces redundancy to improve read performance at the cost of update complexity?",
            "options": ["Normalization", "Denormalization", "Indexing", "Partitioning"],
            "answer": "Denormalization",
            "feedback_correct": (
                "Correct. Denormalization deliberately combines normalized tables or adds "
                "redundant columns to reduce the number of JOINs for frequent read queries."
            ),
            "feedback_wrong": (
                "Not quite. Denormalization is the intentional reversal of some normalization "
                "steps — trading write anomaly risk for faster reads."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "The implant schema is before you. You must identify the update anomaly and "
                "choose the redesign that correctly normalizes away the problem."
            ),
            "task": "Complete the schema surgery: choose the design that removes the functional dependency anomaly.",
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 5 — The Last Broadcast   (Transactions + Concurrency)
    # ──────────────────────────────────────────────────────────────────────────
    5: [
        {
            "type": "read",
            "narrative": (
                "A wildfire is spreading across three districts. Fire Command, Police, and Transit "
                "are each updating overlapping evacuation route records in the same database. "
                "Residents in Zone 7 are receiving three different evacuation routes simultaneously. "
                "Two agencies have already committed. One is mid-transaction. Records contradict each other in real time."
            ),
            "task": "Read the situation report. Proceed to the concurrency analysis.",
        },
        {
            "type": "mcq",
            "narrative": (
                "Transit reads the current route for Zone 7 as 'Highway 4'. Fire Command, in the "
                "middle of updating it to 'Route 12', has not yet committed. Transit sees "
                "'Route 12' and broadcasts it before Fire Command rolls back."
            ),
            "task": "What concurrency anomaly describes reading an uncommitted change from another transaction?",
            "options": ["Lost update", "Non-repeatable read", "Phantom read", "Dirty read"],
            "answer": "Dirty read",
            "feedback_correct": (
                "Correct. A dirty read occurs when a transaction reads data modified by another "
                "transaction that has not yet committed — potentially reading a value that will be rolled back."
            ),
            "feedback_wrong": (
                "Not quite. A dirty read is when you see another transaction's in-progress "
                "changes. If that transaction rolls back, you've read data that never existed."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Police reads the Zone 7 route twice in the same transaction — first returning "
                "'Highway 4', then 'Route 12' — because Fire Command committed a change between "
                "the two reads."
            ),
            "task": "What anomaly causes the same row to return different values when read twice within the same transaction?",
            "options": ["Dirty read", "Non-repeatable read", "Phantom read", "Lost update"],
            "answer": "Non-repeatable read",
            "feedback_correct": (
                "Correct. A non-repeatable read occurs when a row is read twice in the same "
                "transaction but returns different values because another committed transaction "
                "modified it between the reads."
            ),
            "feedback_wrong": (
                "Not quite. Non-repeatable read: read the same row twice in one transaction, "
                "get different values both times due to another committed update."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Fire Command queries 'all open evacuation routes in Zone 7' — gets 3. "
                "It assigns resources. Transit inserts a new route. "
                "Fire Command re-queries — now there are 4. Its resource assignment is stale."
            ),
            "task": "What anomaly describes a query returning different rows due to inserts or deletes by another committed transaction?",
            "options": ["Lost update", "Non-repeatable read", "Dirty read", "Phantom read"],
            "answer": "Phantom read",
            "feedback_correct": (
                "Correct. A phantom read occurs when a transaction re-executes a query and finds "
                "a different number of rows because another transaction inserted or deleted "
                "rows matching the predicate."
            ),
            "feedback_wrong": (
                "Not quite. A phantom read is caused by INSERT or DELETE (not UPDATE) — new rows "
                "'appear' in the result set between two reads of the same query."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "To prevent dirty reads without full serializability costs, the database offers "
                "an isolation level that only shows data from committed transactions."
            ),
            "task": "Which isolation level prevents dirty reads but still allows non-repeatable and phantom reads?",
            "options": [
                "Read Uncommitted",
                "Read Committed",
                "Repeatable Read",
                "Serializable",
            ],
            "answer": "Read Committed",
            "feedback_correct": (
                "Correct. Read Committed ensures you only see committed data — preventing dirty "
                "reads — but doesn't protect against non-repeatable or phantom reads."
            ),
            "feedback_wrong": (
                "Not quite. The four isolation levels are: Read Uncommitted < Read Committed < "
                "Repeatable Read < Serializable. Read Committed blocks dirty reads only."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Fire Command holds an X-lock on Zone 7 and waits for Zone 12. "
                "Transit holds Zone 12 and waits for Zone 7. "
                "Neither can proceed."
            ),
            "task": "What is this situation — two transactions each holding a lock the other needs — called?",
            "options": ["Starvation", "Livelock", "Deadlock", "Race condition"],
            "answer": "Deadlock",
            "feedback_correct": (
                "Correct. A deadlock is a circular wait: T1 holds what T2 needs, and T2 holds "
                "what T1 needs. Neither can proceed without the other releasing first."
            ),
            "feedback_wrong": (
                "Not quite. A deadlock is a circular lock dependency — both transactions are "
                "actively waiting for each other indefinitely."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The DBMS detects the deadlock after 500ms by inspecting the wait-for graph. "
                "It must break the cycle by choosing one transaction to abort."
            ),
            "task": "What is the standard DBMS approach to resolving a deadlock?",
            "options": [
                "Wait indefinitely until one transaction times out",
                "Abort both transactions",
                "Select a victim transaction and roll it back",
                "Upgrade the lock type for both transactions",
            ],
            "answer": "Select a victim transaction and roll it back",
            "feedback_correct": (
                "Correct. The DBMS picks a victim — typically the transaction with least work "
                "done — and rolls it back to break the deadlock."
            ),
            "feedback_wrong": (
                "Not quite. The DBMS detects the cycle with a wait-for graph, selects a "
                "victim, and rolls it back. The victim is then retried."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "Two emergency agencies are simultaneously reserving the same evacuation route. "
                "You must select the correct concurrency control policy to prevent the lost "
                "update without causing a deadlock."
            ),
            "task": "Use the locking simulator to choose the right policy and prevent the race condition.",
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 6 — The Depth Ledger   (Advanced SQL)
    # ──────────────────────────────────────────────────────────────────────────
    6: {
        "format": "episodic",
        "episodes": [
            [
                {"type": "story", "text": "A cache of 200,000 digitised clay tablets reveals merchant trade data spanning three centuries of the Veridian Empire."},
                {"type": "problem", "text": "The archive is chaotic. Tablets are piled everywhere with no structure."},
                {"type": "concept", "title": "Tables, Rows, & Columns", "explanation": "A database organizes data into Tables (entities). Each Row is a single record, and each Column is an attribute."},
                {"type": "micro_challenge", "challenge_type": "mcq", "task": "If a tablet lists 'Aster, Copper, 500 units', what does this represent?", "options": ["A table", "A row", "A column"], "answer": "A row"}
            ],
            [
                {"type": "story", "text": "We've organized the tablets into a pile for 'Merchants' and a pile for 'Transactions'."},
                {"type": "problem", "text": "Wait... two merchants are both named 'Aster'. How do we know which Aster made which transaction?"},
                {"type": "concept", "title": "Primary Keys", "explanation": "A Primary Key (PK) is a column that uniquely identifies every row in a table."},
                {"type": "micro_challenge", "challenge_type": "mcq", "task": "Which of these is the best Primary Key for the Merchants table?", "options": ["Name", "City", "Merchant_ID (Unique Number)"], "answer": "Merchant_ID (Unique Number)"}
            ],
            [
                {"type": "story", "text": "Now every merchant has a Merchant_ID (e.g. Aster is ID 1)."},
                {"type": "problem", "text": "How do we record that Aster (ID 1) made a transaction without writing 'Aster' again?"},
                {"type": "concept", "title": "Foreign Keys", "explanation": "A Foreign Key (FK) is a column in one table that references the Primary Key of another table, creating a relationship."},
                {"type": "micro_challenge", "challenge_type": "mcq", "task": "In the Transactions table, which column acts as the Foreign Key?", "options": ["Transaction_ID", "Merchant_ID", "Amount"], "answer": "Merchant_ID"}
            ],
            [
                {"type": "story", "text": "Aster moves from North City to East City. We have 10,000 transactions for Aster."},
                {"type": "problem", "text": "If we stored 'City' in every transaction row, we'd have to update 10,000 rows. If we miss one, the data contradicts itself!"},
                {"type": "concept", "title": "Update Anomaly", "explanation": "When duplicate data isn't updated everywhere, the database becomes inconsistent."},
                {"type": "micro_challenge", "challenge_type": "mcq", "task": "How do we prevent this anomaly?", "options": ["Store City in the Transactions table", "Store City only in the Merchants table", "Never let Aster move"], "answer": "Store City only in the Merchants table"}
            ],
            [
                {"type": "story", "text": "We need to design a clean schema before we query for the conspiracy."},
                {"type": "problem", "text": "The raw data has multiple values in one cell: Goods = 'Copper, Grain'."},
                {"type": "concept", "title": "Normalization (1NF)", "explanation": "First Normal Form requires that every column holds exactly one value (atomic values)."},
                {"type": "micro_challenge", "challenge_type": "mcq", "task": "How do we fix the Goods column?", "options": ["Create separate rows for each good", "Leave it comma-separated"], "answer": "Create separate rows for each good"}
            ],
            [
                {"type": "story", "text": "The data is clean, normalized, and linked. We suspect fraud among the merchants."},
                {"type": "problem", "text": "We need to find the merchants with the highest trade totals."},
                {"type": "concept", "title": "Advanced SQL: GROUP BY", "explanation": "We can use GROUP BY to collapse all transactions for each merchant and SUM() their amounts."},
                {"type": "interactive", "task": "Use the SQL terminal to find the merchants with the highest cumulative trade amounts. Submit your result."}
            ]
        ]
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 7 — The Colony That Forgot Its Laws   (Consensus + Replication)
    # ──────────────────────────────────────────────────────────────────────────
    7: [
        {
            "type": "read",
            "narrative": (
                "The Veridian Colony Network consists of 12 autonomous robot sectors. Each holds "
                "a local copy of the Colony Rulebook — 4,000 governance laws. Six hours ago, "
                "Sector 3 updated Article 7 (resource allocation). Sector 9 simultaneously "
                "updated Article 7 with a conflicting rule. Both updates were committed locally. "
                "Two robots are about to make opposite decisions and both believe their law is authoritative."
            ),
            "task": "Read the situation. Proceed to the replication analysis.",
        },
        {
            "type": "mcq",
            "narrative": (
                "Each sector holds a copy of the Rulebook. Updates made in one sector must "
                "propagate to all others. This is a core problem in distributed database design."
            ),
            "task": "What is database replication?",
            "options": [
                "Splitting a database across multiple machines by rows",
                "Maintaining multiple copies of the same data across different nodes",
                "Compressing data for faster transfer",
                "Normalizing a database to remove redundancy",
            ],
            "answer": "Maintaining multiple copies of the same data across different nodes",
            "feedback_correct": (
                "Correct. Replication keeps synchronised copies of data on multiple nodes, "
                "improving availability and read throughput — at the cost of consistency complexity."
            ),
            "feedback_wrong": (
                "Not quite. Replication = copies on multiple nodes. "
                "Partitioning/sharding = split rows across nodes. Different problems."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The most common replication model designates one node as the primary writer. "
                "All writes go through it; other nodes receive the change stream and apply it."
            ),
            "task": "In leader/follower (primary/replica) replication, which node accepts write operations?",
            "options": [
                "Any node",
                "The follower nodes only",
                "The leader (primary) node only",
                "Whichever node is least loaded",
            ],
            "answer": "The leader (primary) node only",
            "feedback_correct": (
                "Correct. In leader/follower replication, the leader accepts all writes. "
                "Followers are read-only replicas that receive a replication stream."
            ),
            "feedback_wrong": (
                "Not quite. The leader/primary is the single write authority. "
                "Followers are read-only — this prevents conflicting concurrent writes."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Sector 1's leader node goes offline due to a power failure. Followers have "
                "copies but cannot accept writes without a new leader. The cluster must elect one."
            ),
            "task": "What process promotes a follower node to leader when the current leader fails?",
            "options": ["Sharding", "Rebalancing", "Failover", "Defragmentation"],
            "answer": "Failover",
            "feedback_correct": (
                "Correct. Failover is the process of detecting a leader failure and promoting "
                "a follower to serve as the new leader, restoring write availability."
            ),
            "feedback_wrong": (
                "Not quite. Failover is the automated (or manual) handover from a failed leader "
                "to a new leader — requiring failure detection and follower promotion."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "A follower that is 14 seconds behind the leader is accidentally promoted. "
                "The colony loses 14 seconds of committed law changes on failover."
            ),
            "task": "What term describes the maximum data loss window when failing over to a replica?",
            "options": [
                "Replication lag",
                "RPO (Recovery Point Objective)",
                "RTO (Recovery Time Objective)",
                "MTBF",
            ],
            "answer": "RPO (Recovery Point Objective)",
            "feedback_correct": (
                "Correct. RPO is the maximum acceptable data loss measured in time. "
                "A 14-second lag means up to 14 seconds of committed writes could be lost."
            ),
            "feedback_wrong": (
                "Not quite. RPO defines how much data loss is tolerable. RTO defines how long "
                "the system can be unavailable. The lag in this scenario is an RPO concern."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "To prevent conflicting writes, the system requires that any law change be "
                "acknowledged by at least 7 of 12 sectors before it is considered committed."
            ),
            "task": "In a quorum-based system, what is the minimum number of nodes that must agree for a decision to commit?",
            "options": [
                "Any one node",
                "All nodes",
                "A majority (more than half)",
                "Exactly two nodes",
            ],
            "answer": "A majority (more than half)",
            "feedback_correct": (
                "Correct. A quorum requires a majority (⌊n/2⌋ + 1) to agree. "
                "This prevents split-brain: no two conflicting majorities can form simultaneously."
            ),
            "feedback_wrong": (
                "Not quite. A quorum is defined as ⌊n/2⌋ + 1 — more than half. "
                "This mathematical constraint makes it impossible for two conflicting majorities to coexist."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Sector 3 and Sector 9 simultaneously propose different values for Article 7. "
                "With 12 sectors and a quorum of 7, each proposal needs 7 votes. "
                "It is mathematically impossible for both to reach quorum simultaneously."
            ),
            "task": "What property of quorum systems prevents two conflicting proposals from both being committed?",
            "options": [
                "Quorums are always processed sequentially",
                "Any two quorums must overlap — they share at least one member",
                "Only the leader can initiate proposals",
                "All nodes must vote for the same proposal",
            ],
            "answer": "Any two quorums must overlap — they share at least one member",
            "feedback_correct": (
                "Correct. Any two majorities of n nodes must share at least one common member. "
                "That node cannot vote for both proposals — preventing simultaneous conflicting commits."
            ),
            "feedback_wrong": (
                "Not quite. The guarantee: if two quorums could be disjoint, both could commit. "
                "Since both are majorities of the same total, they must overlap."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "The 12 sectors are live. Sector 3 has proposed a new law. "
                "You must configure the quorum size and gather enough votes to determine "
                "whether the proposal can be safely committed."
            ),
            "task": "Use the replica consensus simulator to reach quorum and commit the law.",
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 8 — The Machine That Lied   (MVCC + Isolation)
    # ──────────────────────────────────────────────────────────────────────────
    8: [
        {
            "type": "read",
            "narrative": (
                "ARIA, an AI decision system, generated two briefings from the same report database. "
                "Department A received a briefing stating the project budget is $4.2M. "
                "Department B received one stating it is $3.8M — generated 11 minutes later. "
                "ARIA's logs insist it never produced contradictory output. "
                "Both departments have authenticated screenshots. The truth is in the version history."
            ),
            "task": "Read the incident summary. Proceed to the MVCC investigation.",
        },
        {
            "type": "mcq",
            "narrative": (
                "The report database allows concurrent read transactions while a write transaction "
                "updates a row. Rather than blocking readers, it stores the old version "
                "alongside the new one."
            ),
            "task": "What concurrency control mechanism allows readers to see a consistent snapshot without blocking on writers?",
            "options": [
                "Two-Phase Locking (2PL)",
                "Multi-Version Concurrency Control (MVCC)",
                "Optimistic Locking",
                "Timestamp Ordering",
            ],
            "answer": "Multi-Version Concurrency Control (MVCC)",
            "feedback_correct": (
                "Correct. MVCC maintains multiple versions of a row. Readers see a version "
                "consistent with their transaction start time; writers create new versions — no blocking required."
            ),
            "feedback_wrong": (
                "Not quite. MVCC (used by PostgreSQL, Oracle, MySQL InnoDB) keeps old row versions "
                "so readers can access their consistent snapshot without waiting for writers."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "T1 started at t=0. Budget writer T2 committed $3.8M → $4.2M at t=5. "
                "T1 reads at t=8 and sees $4.2M. "
                "T3 started at t=2 and reads at t=9."
            ),
            "task": "Under Snapshot Isolation, which budget value does T3 (started at t=2) see when it reads at t=9?",
            "options": [
                "$4.2M — the latest committed version",
                "$3.8M — the version that existed when T3 started",
                "An error — the row is locked",
                "NULL — the version has been garbage collected",
            ],
            "answer": "$3.8M — the version that existed when T3 started",
            "feedback_correct": (
                "Correct. Under Snapshot Isolation, T3 sees the database as it was at its start "
                "time (t=2), before T2 committed at t=5 — so it sees $3.8M."
            ),
            "feedback_wrong": (
                "Not quite. Snapshot Isolation takes a snapshot at transaction start. "
                "T3 started before the t=5 commit, so its snapshot contains the pre-update $3.8M."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "This explains both briefings: T1 and T3 ran under Snapshot Isolation with "
                "different start times, giving each a consistent but different view of the same row."
            ),
            "task": "What isolation anomaly does Snapshot Isolation still allow, despite preventing most others?",
            "options": [
                "Dirty reads",
                "Non-repeatable reads",
                "Write skew",
                "Phantom reads from inserts",
            ],
            "answer": "Write skew",
            "feedback_correct": (
                "Correct. Snapshot Isolation prevents dirty reads, non-repeatable reads, and most "
                "phantoms — but allows write skew: two transactions read overlapping data and make "
                "conflicting updates that each appear valid in isolation."
            ),
            "feedback_wrong": (
                "Not quite. Write skew is Snapshot Isolation's main weakness: T1 and T2 each read "
                "a constraint, see it satisfied in their snapshot, and write values that together violate it."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The database keeps multiple versions of every row. Over time, old versions "
                "no longer needed by any active transaction must be reclaimed."
            ),
            "task": "What background process removes row versions no longer visible to any active transaction?",
            "options": [
                "Checkpointing",
                "Vacuuming / garbage collection",
                "Defragmentation",
                "Log archiving",
            ],
            "answer": "Vacuuming / garbage collection",
            "feedback_correct": (
                "Correct. PostgreSQL calls this VACUUM; other MVCC systems call it garbage "
                "collection. Without it, dead row versions accumulate and waste storage."
            ),
            "feedback_wrong": (
                "Not quite. MVCC creates dead row versions on every update. Without a vacuum/GC "
                "process, the database would grow indefinitely."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After the incident, the company wants to query the database as it appeared at "
                "any past point in time — for compliance and audit."
            ),
            "task": "What database feature allows querying the historical state of data at any past timestamp?",
            "options": [
                "A foreign key with ON DELETE SET NULL",
                "A materialized view",
                "Temporal tables / bi-temporal data",
                "An event-sourcing log",
            ],
            "answer": "Temporal tables / bi-temporal data",
            "feedback_correct": (
                "Correct. Temporal tables (SQL:2011 standard) record valid-time and "
                "transaction-time for every row, enabling AS OF queries like: "
                "SELECT * FROM report AS OF TIMESTAMP '...'."
            ),
            "feedback_wrong": (
                "Not quite. Temporal tables store when data was valid and when it was recorded "
                "— enabling full historical reconstruction."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The audit team wants every write to the report database logged with who, when, "
                "and from which transaction — creating a tamper-evident history, "
                "without requiring application code changes."
            ),
            "task": "What database mechanism automatically records changes with a timestamp and user context?",
            "options": ["A constraint", "A trigger", "An index", "A view"],
            "answer": "A trigger",
            "feedback_correct": (
                "Correct. A trigger fires automatically on INSERT, UPDATE, or DELETE and can "
                "write an audit record to a history table, capturing who, what, and when."
            ),
            "feedback_wrong": (
                "Not quite. Triggers are the database-native way to intercept writes and produce "
                "audit records without requiring application code changes."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "The MVCC timeline for the report database is reconstructed. "
                "You can see T1, T2, and T3 and their overlapping lifetimes. "
                "Change the isolation level and replay the timeline."
            ),
            "task": "Use the MVCC timeline viewer to demonstrate that Snapshot Isolation caused both departments to see different committed values.",
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 9 — The Forgotten Archive   (DBMS Foundations)
    # ──────────────────────────────────────────────────────────────────────────
    9: [
        {
            "type": "read",
            "narrative": (
                "The Veridian Museum of Cultural Heritage maintains four paper-ledger systems: "
                "a Visitor Registry, Artifact Catalog, Loan Record, and Curator Directory. "
                "Each is managed by a different department. Last week, Curator Elin updated an "
                "artifact's origin date in the Catalog — but the Loan Record still shows the "
                "old date. A visiting researcher is now questioning the integrity of the entire archive."
            ),
            "task": "Read the case. Proceed to analyze the file-based system's weaknesses.",
        },
        {
            "type": "mcq",
            "narrative": (
                "The Loan Record stores the artifact's origin date inline — a copy from the "
                "Artifact Catalog. Updating the Catalog requires manually updating every other "
                "file that copied that field."
            ),
            "task": "What problem occurs when application programs are tightly coupled to the physical structure of data files?",
            "options": [
                "Data redundancy",
                "Data dependency",
                "Schema drift",
                "Referential integrity violation",
            ],
            "answer": "Data dependency",
            "feedback_correct": (
                "Correct. Data dependency means programs must know the physical details of data "
                "storage. Any change to the file format or location breaks the programs that use it."
            ),
            "feedback_wrong": (
                "Not quite. Data dependency: programs are written to specific file layouts. "
                "Move or restructure the file, and all programs break. DBMS abstraction solves this."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "A DBMS introduces a layer of abstraction between applications and physical "
                "data storage. Programs ask for data by name; the DBMS handles physical location and format."
            ),
            "task": "What type of independence allows the physical storage structure to change without requiring changes to application programs?",
            "options": [
                "Logical data independence",
                "Physical data independence",
                "Schema independence",
                "Program independence",
            ],
            "answer": "Physical data independence",
            "feedback_correct": (
                "Correct. Physical data independence means you can change how data is stored "
                "(file layout, indexes, compression) without affecting applications or the conceptual schema."
            ),
            "feedback_wrong": (
                "Not quite. Physical = changing storage without breaking programs. "
                "Logical = changing the logical schema without breaking external views/programs."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The ANSI/SPARC three-schema architecture defines three distinct levels of "
                "database description, each serving a different audience."
            ),
            "task": "How many schema levels does the ANSI/SPARC three-schema architecture define?",
            "options": ["2", "3", "4", "5"],
            "answer": "3",
            "feedback_correct": (
                "Correct. The three levels are: External (user views), Conceptual (logical "
                "structure), and Internal (physical storage)."
            ),
            "feedback_wrong": (
                "Not quite. The architecture has exactly 3 levels: External, Conceptual, Internal."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The museum curator interacts with a form showing artifact name, origin date, and "
                "loan status — a simplified view tailored to their role. "
                "They never see the physical tables or storage structure."
            ),
            "task": "Which schema level defines user-specific views — what individual users or applications can see?",
            "options": [
                "Internal schema",
                "Conceptual schema",
                "External schema",
                "Storage schema",
            ],
            "answer": "External schema",
            "feedback_correct": (
                "Correct. The external schema (also called the view level) defines the portion of "
                "the database visible to specific users or application programs."
            ),
            "feedback_wrong": (
                "Not quite. External schema = user views and application interfaces. "
                "Different users can have different external schemas of the same database."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Behind the curator's view, the database defines all entities and relationships: "
                "Artifacts, Curators, Visitors, Loans — with constraints, relationships, and data types. "
                "This is the complete logical picture."
            ),
            "task": "Which schema level defines the overall logical structure — all entities, attributes, and relationships?",
            "options": [
                "External schema",
                "Conceptual schema",
                "Internal schema",
                "Physical schema",
            ],
            "answer": "Conceptual schema",
            "feedback_correct": (
                "Correct. The conceptual schema is the community view — all data, all "
                "relationships, all constraints — independent of any physical storage details."
            ),
            "feedback_wrong": (
                "Not quite. The conceptual schema is the logical blueprint: what data exists "
                "and how it relates, independent of both user views and storage details."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Beneath the logical structure, the DBMS decides how to store data on disk: "
                "which blocks each table occupies, file format, compression, and indexes."
            ),
            "task": "Which schema level describes the physical storage of data — file formats, page layouts, and index structures?",
            "options": [
                "External schema",
                "Conceptual schema",
                "Internal schema",
                "Logical schema",
            ],
            "answer": "Internal schema",
            "feedback_correct": (
                "Correct. The internal schema defines the physical representation: storage "
                "structures, access paths, file organization, and index definitions."
            ),
            "feedback_wrong": (
                "Not quite. The internal schema is the lowest level — closest to the hardware. "
                "It defines exactly how data is physically stored."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "The museum's three-schema architecture has been scrambled. You must match each "
                "schema level to its correct responsibility to restore the archive."
            ),
            "task": "Complete the three-schema architecture puzzle: assign External, Conceptual, and Internal to their correct roles.",
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 10 — The Blueprint That Couldn't Exist   (ER + Relational theory)
    # ──────────────────────────────────────────────────────────────────────────
    10: [
        {
            "type": "read",
            "narrative": (
                "City Architect Rael submitted blueprints for a new district. "
                "The planning committee's algorithm flagged 14 buildings as 'impossible' — "
                "they violate the city's own structural laws. The laws are stored as "
                "entity-relationship constraints. Your task: model the city correctly "
                "and determine which buildings cannot legally exist under the relational rules."
            ),
            "task": "Read the architectural brief. Proceed to the ER analysis.",
        },
        {
            "type": "mcq",
            "narrative": (
                "The blueprint defines objects: Building, District, Architect, Material. "
                "Each has properties and identifiers. The ER model represents these as entities."
            ),
            "task": "In an Entity-Relationship (ER) diagram, what is an entity?",
            "options": [
                "A relationship between two tables",
                "A real-world object or concept that has an existence independent of other objects",
                "A column in a database table",
                "A constraint on data values",
            ],
            "answer": "A real-world object or concept that has an existence independent of other objects",
            "feedback_correct": (
                "Correct. An entity is a distinguishable object in the real world — a thing "
                "with its own identity, like Building, Person, or Product."
            ),
            "feedback_wrong": (
                "Not quite. An entity is a thing with independent existence (Building, Architect). "
                "A relationship (designs) connects entities. Attributes describe entities."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The city law states: each building is designed by exactly one architect, "
                "but an architect can design many buildings."
            ),
            "task": "What term describes the numerical relationship between entity instances — one architect to many buildings?",
            "options": ["Specialization", "Cardinality", "Participation", "Aggregation"],
            "answer": "Cardinality",
            "feedback_correct": (
                "Correct. Cardinality defines how many instances of one entity can relate to "
                "instances of another: 1:1, 1:N, or M:N."
            ),
            "feedback_wrong": (
                "Not quite. Cardinality specifies the count of entity instances on each side "
                "of a relationship: one-to-one, one-to-many, or many-to-many."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The blueprint includes Residential_Building and Commercial_Building — both share "
                "Building attributes (address, height, material) but have unique properties "
                "(occupant_count vs. commercial_zone)."
            ),
            "task": "What ER modeling concept captures shared attributes in a parent entity while unique attributes exist in child entities?",
            "options": [
                "Aggregation",
                "Weak entity",
                "Generalization / specialization",
                "Participation constraint",
            ],
            "answer": "Generalization / specialization",
            "feedback_correct": (
                "Correct. Generalization combines common attributes into a supertype (Building). "
                "Specialization creates subtypes (Residential, Commercial) with additional attributes."
            ),
            "feedback_wrong": (
                "Not quite. Generalization/specialization is the ER equivalent of class "
                "inheritance — supertype holds shared attributes; subtypes hold specialized ones."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "You need to find all buildings in the 'North' district. In relational algebra, "
                "you must extract only the rows where district = 'North'."
            ),
            "task": "Which relational algebra operation filters rows based on a condition?",
            "options": [
                "Projection (π)",
                "Selection (σ)",
                "Join (⋈)",
                "Union (∪)",
            ],
            "answer": "Selection (σ)",
            "feedback_correct": (
                "Correct. Selection (σ) filters tuples (rows) from a relation based on a "
                "predicate: σ_{district='North'}(Building) returns only North district buildings."
            ),
            "feedback_wrong": (
                "Not quite. Selection = filter rows (horizontal slice). "
                "Projection = filter columns (vertical slice). Join = combine two relations."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "From the buildings in 'North' district, you only need building_id and height "
                "— not all 12 attributes."
            ),
            "task": "Which relational algebra operation selects only certain columns from a relation?",
            "options": [
                "Selection (σ)",
                "Projection (π)",
                "Cartesian product (×)",
                "Difference (−)",
            ],
            "answer": "Projection (π)",
            "feedback_correct": (
                "Correct. Projection (π) keeps only specified attributes: "
                "π_{building_id, height}(Building) returns only those two columns."
            ),
            "feedback_wrong": (
                "Not quite. Projection = column selection (vertical slice). "
                "Selection = row filtering (horizontal slice)."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "To answer 'which architects designed buildings in the North district?', you need "
                "data from both Building and Architect relations. They share architect_id."
            ),
            "task": "Which relational algebra operation combines tuples from two relations that share matching attributes?",
            "options": [
                "Union",
                "Difference",
                "Natural join",
                "Cartesian product",
            ],
            "answer": "Natural join",
            "feedback_correct": (
                "Correct. A natural join combines relations on matching attribute names/values, "
                "eliminating duplicate attribute columns."
            ),
            "feedback_wrong": (
                "Not quite. A natural join combines on matching attributes. "
                "A Cartesian product pairs every row with every other row regardless of condition."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "The city's entity model is before you. Select the correct relational algebra "
                "operation to answer the planning committee's query about the North district buildings."
            ),
            "task": "Apply the correct relational algebra operation to find the buildings that violate the city's structural laws.",
        },
    ],

    # ──────────────────────────────────────────────────────────────────────────
    # 11 — The Impossible Contract   (1NF–5NF + SQL)
    # ──────────────────────────────────────────────────────────────────────────
    11: [
        {
            "type": "read",
            "narrative": (
                "The Meridian Legal Archive holds 11,000 digitised contracts. A billion-dollar "
                "case depends on a clause from Contract 4471 — but the archive contains three "
                "conflicting versions stored in differently structured tables. Legal analysts "
                "cannot determine which is authoritative. The contradiction is not fraud: "
                "it is a schema design problem."
            ),
            "task": "Read the case briefing. Proceed to the normalization analysis.",
        },
        {
            "type": "mcq",
            "narrative": (
                "The clauses table contains a 'parties' column with the value "
                "'Aster Corp, Borin Ltd, Cyra Inc' — three party names in a single cell. "
                "Searching for 'Borin Ltd' requires LIKE '%Borin%' — no index possible."
            ),
            "task": "Which normal form is violated when a column contains multiple values (a list or set) in a single cell?",
            "options": ["2NF", "3NF", "1NF", "BCNF"],
            "answer": "1NF",
            "feedback_correct": (
                "Correct. 1NF requires atomic values — each column must hold a single, "
                "indivisible value. Comma-separated lists violate 1NF."
            ),
            "feedback_wrong": (
                "Not quite. 1NF is the first rule: atomic values only. "
                "No lists, no sets, no repeating groups in a single cell."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After atomizing the parties, the primary key is (contract_id, party_id). "
                "The column 'contract_title' depends only on contract_id — it repeats "
                "identically for every party in the contract."
            ),
            "task": "Which normal form requires every non-key attribute to depend on the ENTIRE primary key, not just part of it?",
            "options": ["1NF", "2NF", "3NF", "4NF"],
            "answer": "2NF",
            "feedback_correct": (
                "Correct. 2NF eliminates partial dependencies. contract_title depends on "
                "contract_id alone — it belongs in a separate Contracts table."
            ),
            "feedback_wrong": (
                "Not quite. 2NF applies when there is a composite key. Every non-key attribute "
                "must depend on the whole key, not a subset."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After 2NF, the contracts table has: contract_id, contract_title, law_firm_id, "
                "law_firm_address. Law_firm_address depends on law_firm_id — a transitive chain "
                "through a non-key attribute."
            ),
            "task": "Which normal form eliminates transitive dependencies between non-key attributes?",
            "options": ["1NF", "2NF", "3NF", "BCNF"],
            "answer": "3NF",
            "feedback_correct": (
                "Correct. 3NF requires non-key attributes to depend only on the primary key. "
                "Law_firm_address should live in a separate LawFirms table."
            ),
            "feedback_wrong": (
                "Not quite. 3NF eliminates: contract_id → law_firm_id → law_firm_address. "
                "That last step is transitive and must be separated."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "After 3NF, clause_author → law_firm_id exists, but clause_author is not a "
                "candidate key. BCNF requires every determinant to be a superkey."
            ),
            "task": "What does fixing a BCNF violation require?",
            "options": [
                "Adding a composite primary key",
                "Decomposing the relation so the determinant becomes a key in its own table",
                "Adding a CHECK constraint",
                "Removing the dependent attribute",
            ],
            "answer": "Decomposing the relation so the determinant becomes a key in its own table",
            "feedback_correct": (
                "Correct. The fix for a BCNF violation is decomposition — extract the violating "
                "FD into a new relation where the determinant is the primary key."
            ),
            "feedback_wrong": (
                "Not quite. BCNF is fixed by decomposition: extract X → Y (where X is not a "
                "superkey) into a new relation where X is the key."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "The archive also stores: for each (supplier, product), the supplier is certified "
                "by multiple certifying bodies independently. This creates a multi-valued "
                "dependency that causes redundancy even in BCNF."
            ),
            "task": "Which normal form eliminates multi-valued dependencies — where one attribute independently determines a set of values for another?",
            "options": ["3NF", "BCNF", "4NF", "5NF"],
            "answer": "4NF",
            "feedback_correct": (
                "Correct. 4NF eliminates multi-valued dependencies. "
                "If A →→ B and A →→ C independently, {A,B} and {A,C} should be stored in separate tables."
            ),
            "feedback_wrong": (
                "Not quite. 4NF handles multi-valued dependencies (MVDs), written as A →→ B. "
                "They arise when one attribute independently determines sets of values for two others."
            ),
        },
        {
            "type": "mcq",
            "narrative": (
                "Even after 4NF, a join dependency remains: the table (Supplier, Product, Certifier) "
                "can only be losslessly decomposed into three projections — not two."
            ),
            "task": "Which normal form addresses join dependencies that cannot be decomposed into fewer relations without information loss?",
            "options": ["3NF", "BCNF", "4NF", "5NF"],
            "answer": "5NF",
            "feedback_correct": (
                "Correct. 5NF (Project-Join Normal Form, PJNF) eliminates join dependencies. "
                "A relation is in 5NF if every join dependency is implied by the candidate keys."
            ),
            "feedback_wrong": (
                "Not quite. 5NF deals with join dependencies — the most subtle redundancy, "
                "where decomposing into two projections loses information only a three-way join restores."
            ),
        },
        {
            "type": "interactive",
            "narrative": (
                "The normalization ladder is before you. The contract archive can be fully "
                "resolved only if you apply all six normal forms in the correct sequence. "
                "One wrong step and the schema remains corrupted."
            ),
            "task": "Arrange the normalization forms in the correct order to unlock the full ladder and resolve Contract 4471.",
        },
    ],
}
