# Interview Prep — using TradeLens as the artifact

## The 90-second project story

Drill this format until it's automatic. Most candidates describe *what they built*; almost none describe *what they decided*.

1. **Context (1 sentence)** — "TradeLens is a streaming pipeline that evaluates paper-trading execution quality against live market data."
2. **The hard part (1 sentence)** — the constraint that made it non-trivial. Not "I used Kafka." Rather: "Order state changes and market ticks arrive on different clocks, so naive joins produced wrong fill benchmarks."
3. **The decision + the rejected alternative** — "I used Debezium CDC off the Postgres WAL rather than dual-writing from the app, because dual-writes lose atomicity between the DB commit and the Kafka publish."
4. **The number** — end-to-end latency, throughput, consumer lag, query p99, rows scanned. Any number. Measure one if he doesn't have one.
5. **What he'd do differently** — self-awareness reads as seniority. "No schema registry yet; a column rename would break consumers silently."

Make him say it out loud. Written answers hide the parts he can't actually explain.

## Decisions in TradeLens worth being able to defend

Interviewers probe the seams. He should have a crisp answer for each:

- Why ClickHouse for analytics instead of just querying Postgres?
- Why CDC instead of the app dual-writing to Kafka?
- Why event time (`trade_ts`) and not processing time (`ingested_at`) for OHLCV windows? What breaks if you get it wrong?
- What's his delivery guarantee, and where could a trade be double-counted?
- Why materialized views in ClickHouse instead of Airflow batch jobs? (What are MVs *actually* — insert-time triggers, not cached queries.)
- How does he handle late-arriving ticks?
- Could he rebuild ClickHouse from scratch today? How long would it take?
- Where does auth actually get enforced — and is any check client-side only?

## What US internship recruiters screen on

Honest ordering, for a competitive market:

1. **Reachable evidence** — a live URL, a public repo with a README that explains itself in 60 seconds, a demo GIF. A private repo with 200 commits is worth less than a deployed toy.
2. **Depth in one thing** — TradeLens is his depth. Better to have one system he can discuss for 45 minutes than five tutorials.
3. **DSA screen** — most US internship funnels still gate on an online assessment. This is separate practice; the project doesn't substitute for it. Steady low-volume practice beats cramming.
4. **Resume mechanics** — one page, bullets as `<action> <system> <result with number>`, no "responsible for". ATS-parseable (no columns, no tables, no images).
5. **Timing** — US summer internship recruiting front-loads hard; many big-company postings open in the late summer/early fall for the *following* summer, and close before the deadline suggests. Applying early beats applying polished-but-late.
6. **Work authorization** — be upfront in applications about visa/CPT status; wasted interview cycles hurt both sides. Filter for companies that sponsor or for roles that accept his status.

## Coaching stance on this

- Be honest about gaps. Telling him a tutorial-grade feature is impressive wastes his remaining runway.
- Push measurement over features. "Add a number to the README" beats "add another endpoint" almost every time.
- When he finishes something, ask for the 90-second story *before* moving on. The log entry in `docs/learning-log.md` is the raw material for it.
- He is a data engineer breaking into a market that mostly posts SWE internships. His edge is that he can build the pipeline *and* the app — make sure the project shows both halves, and that the web half doesn't look bolted on.
