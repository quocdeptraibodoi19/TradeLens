# Vetted Resources

Prefer primary docs over tutorials. Give him **one** link at a time with a reason — a reading list of twelve links gets read zero times. Verify a URL before quoting it if you're unsure; these are stable but the web moves.

## Web fundamentals
- **MDN Web Docs** (developer.mozilla.org) — the reference. HTTP, CORS, cookies, Fetch, CSS layout. Not a tutorial; use it to look things up precisely.
- **web.dev** (web.dev) — Google's practical guides on performance, Core Web Vitals, modern CSS.
- **"How DNS works" / networking posts on jvns.ca** — Julia Evans. Best explanations of the stuff everyone pretends to already know. Her zines on HTTP and debugging are worth the money.
- **High Performance Browser Networking** (hpbn.co, free online) — Ilya Grigorik. Read the HTTP and TLS chapters.

## CSS / layout
- **CSS-Tricks "A Complete Guide to Flexbox" and "…to Grid"** — the two cheat sheets everyone keeps open.
- **joshwcomeau.com** — Josh Comeau. Interactive explanations of stacking contexts, centering, animation. Best-in-class for "why does CSS do that".

## Vue
- **vuejs.org/guide** — the official guide is genuinely good; read Reactivity Fundamentals and Reactivity in Depth, not just the API list.
- **pinia.vuejs.org** — state management, official.
- **router.vuejs.org** — navigation guards matter for his auth flow.
- **Vue School / Vue Mastery** — paid video, good if he prefers video, skippable.

## FastAPI / Python backend
- **fastapi.tiangolo.com** — the tutorial *is* the docs. Do the Security chapter properly.
- **docs.pydantic.dev** — v2 validation, serialization, settings management.
- **"async/await in Python" — realpython.com/async-io-python** — solid mental model of the event loop.
- **docs.sqlalchemy.org** — the 2.0 ORM tutorial, especially session lifecycle and lazy loading (source of most N+1s).

## Auth & security
- **thecopenhagenbook.com** — free, concise, modern guide to auth implementation. Sessions, tokens, cookies, OAuth. Start here.
- **OWASP Cheat Sheet Series** (cheatsheetseries.owasp.org) — Authentication, Session Management, JWT, CSRF. Terse and authoritative.
- **oauth.net/2/** — the authorization-code + PKCE flow, from the source.

## Data engineering / streaming
- **Designing Data-Intensive Applications** — Kleppmann. The single highest-value book for his career. Chapters 7, 8, 11 are directly this project.
- **debezium.io/documentation** — connector config, snapshots, schema changes, the outbox pattern.
- **Confluent blog** (confluent.io/blog) — "Exactly-Once Semantics in Kafka", the streaming-vs-batch series, Kafka internals.
- **clickhouse.com/docs** — MergeTree family, materialized views, and the "Best Practices" section. Also their blog on real-time analytics patterns.
- **DataTalksClub Data Engineering Zoomcamp** (GitHub, free) — good for filling structural gaps, mostly review for him.
- **martinfowler.com** — CDC, event sourcing, strangler-fig. Vocabulary interviewers use.

## Engineering practice
- **12factor.net** — config, logs, backing services. Short, and it explains why his `.env` layout matters.
- **refactoring.guru** — code smells and refactorings, language-agnostic.
- **Google SRE Book** (sre.google/books, free) — SLIs/SLOs, monitoring, postmortems. Read the monitoring chapter before building his Grafana dashboard.
- **testcontainers.com** — real integration tests against real Postgres/Kafka/ClickHouse. Impressive on a resume, genuinely useful.

## Interview prep
- **neetcode.io** — DSA roadmap; the most efficient path through LeetCode patterns.
- **github.com/donnemartin/system-design-primer** — free, comprehensive system design.
- **"Designing Data-Intensive Applications"** again — this is what data-eng system-design interviews are actually drawn from.
- **Pitt CSC × Simplify internship list** (GitHub) — the community-maintained US internship board; search "Summer 20XX Internships GitHub". Check the current year's repo.
