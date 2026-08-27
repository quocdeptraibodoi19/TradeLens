# TradeLens Curriculum

Ordered by what unblocks the most, not by what's most interesting. He is strong on data/infra and weak on web — the ordering reflects that.

## Where he already is

- Postgres + Alembic migrations, ClickHouse + a second Alembic config for CH metadata, Debezium → Kafka CDC, Airflow, Grafana/Prometheus in `infra/`
- FastAPI app in `backend/app` split into `api/services/{auth,dashboard}`, `streams/`, `analytics/workers/`
- Vue 3 + Vite frontend with Pinia-style `stores/`, `views/`, Storybook, and a design-token system in `frontend/src/design-tokens/`

So: the pipeline is the strength. The web layer and the *production discipline* around both are the gap.

## Track A — Web fundamentals he cannot skip

Do these in order; each is a day or two, not a week.

1. **The request lifecycle.** What actually crosses the wire: DNS → TCP/TLS → HTTP request → response. Read the Network tab on his own app until it's boring. *Checkpoint: he can explain a CORS preflight without looking it up.*
2. **HTTP semantics.** Status codes that matter (401 vs 403, 409, 422), idempotency of verbs, caching headers. *Checkpoint: he can say why a retry of his order-placement endpoint is or isn't safe.*
3. **Auth end to end.** Sessions vs JWT, cookie flags (`HttpOnly`, `SameSite`, `Secure`), where XSS and CSRF actually bite, OAuth authorization-code flow. He already has an auth flow in `api/services/auth` — the task is to *audit* it, not rebuild it. *Checkpoint: he can name the attack each cookie flag prevents.*
4. **Browser rendering + CSS layout.** Flexbox and grid, the cascade, why his layout jumps. Enough to stop fighting it.
5. **Vue reactivity model.** `ref`/`reactive`/`computed`/`watch`, the component lifecycle, props down / events up, why mutating a prop is wrong. *Checkpoint: he can predict which components re-render on a store update.*
6. **Client state + data fetching.** Loading/error/empty states, race conditions on rapid navigation, cancellation, optimistic updates. This is where data engineers usually write their worst frontend code.

## Track B — Backend depth (his bridge track)

1. **Async Python for real.** Event loop, what blocks it, why a sync DB driver in an `async def` route kills throughput. Directly relevant to `streams/`.
2. **FastAPI idioms.** Dependency injection, Pydantic v2 models as the contract, response models, background tasks, lifespan events. *Checkpoint: no business logic left in a route function.*
3. **API design.** Pagination (cursor, not offset, for a trade feed), filtering, error envelopes, versioning. His dashboard endpoints are the place to practice.
4. **Serving analytics safely.** The dashboard queries ClickHouse — learn query timeouts, row limits, and why an unbounded `GROUP BY` from a user-controlled param is a footgun.
5. **Realtime delivery.** WebSockets vs SSE vs polling for pushing ticks to the browser. Pick one deliberately and be able to defend it.

## Track C — Production discipline (highest resume ROI, most often skipped)

1. **Tests.** `pytest` for the backend (a real one against a throwaway Postgres via testcontainers or docker-compose), Vitest + a couple of component tests for the frontend. Target the auth flow and one analytics query first.
2. **CI.** GitHub Actions: lint, test, build on every push. A green badge on the README is disproportionately convincing.
3. **Deployment.** Get it on the public internet with a URL a recruiter can click. Frontend on Netlify/Vercel (Storybook already deploys), backend + a slim pipeline on Fly.io/Railway/a small VM. Cost-control the ClickHouse part.
4. **Observability.** He has Prometheus/Grafana already — make one dashboard that answers "is the pipeline healthy?": consumer lag, end-to-end latency (`ingested_at - trade_ts`), error rate, rows/sec.
5. **README that sells.** Architecture diagram, one-command local start, a GIF of it running, the numbers. Assume 60 seconds of a recruiter's attention.

## Track D — Data engineering, sharpened for interviews

He knows this; the goal is to make it *defensible*, not new.

1. **Delivery semantics.** At-least-once vs exactly-once in his own pipeline. Where exactly could a trade be double-counted, and what makes ClickHouse dedup work (`ReplacingMergeTree` + the right sorting key)?
2. **Event time, watermarks, late data.** Already documented in the README — now handle it in code and be able to show the case that breaks.
3. **Schema evolution.** What happens to the Kafka consumers when a Postgres column is added/renamed? Schema registry, or a deliberate contract.
4. **Backfill + replay.** Can he rebuild ClickHouse from Kafka/Postgres from scratch? Practice it once. This exact question comes up in interviews.
5. **ClickHouse internals worth knowing.** MergeTree, sorting key vs primary key, materialized views as insert triggers (not refreshed views), partitioning strategy, `FINAL` and why it's expensive.

## Milestone sequencing

If he asks "what's next" and has no strong preference, the ordering that maximizes internship signal:

1. Ship it publicly (Track C.3) — an unreachable project is invisible
2. README + architecture diagram + numbers (C.5)
3. Tests + CI on the auth flow and one pipeline path (C.1, C.2)
4. One health dashboard (C.4)
5. Then features again — realtime ticks in the UI (B.5) is the most demo-able
