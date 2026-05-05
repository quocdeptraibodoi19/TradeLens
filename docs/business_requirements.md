# Business Requirements

## Purpose

This pipeline exists to evaluate **paper trading strategy performance** on Alpaca against real market conditions sourced from Alpaca's own market data stream.

Alpaca is both the trading playground and the market data source — keeping the benchmark consistent with how fills are actually priced. Everything downstream (Kafka, ClickHouse, the AI chat) exists to answer one core question:

> **Did my trades on Alpaca execute well relative to what the market was actually doing?**

---

## System Overview

The pipeline is built around two ingestion components and two serving layers:

| Component | Role |
|-----------|------|
| **Alpaca Custom Price Alert app** | FastAPI operational app — syncs Alpaca trading data into PostgreSQL, manages price alerts, and serves operational queries |
| **Alpaca Market Data Stream** | WebSocket ingestion service — streams real-time market ticks directly to Kafka |
| **PostgreSQL** | Operational database — source of truth for current state of orders, symbols, and alerts |
| **ClickHouse** | Analytical data warehouse — source of truth for historical performance and market context |

---

## Component 1 — Alpaca Custom Price Alert (Operational App)

A lightweight FastAPI application that serves as the single operational layer between Alpaca and PostgreSQL. It owns three entities and is also the CDC source for the analytics pipeline.

### `symbols` — the reference dimension

Loaded from Alpaca's REST API on startup and refreshed periodically. Tracks which assets are active, tradeable, and on which exchange. All other entities reference this table.

```
TradingClient.get_all_assets()  →  bulk UPSERT  →  symbols table
```

Only `NASDAQ`, `NYSE`, and `ARCA` symbols are loaded — `OTC` is excluded due to low liquidity and no real-time data feed coverage.

### `orders` — your paper trading positions

Ingested in real time from Alpaca's `TradingStream` WebSocket. Every order state transition fires a `TradeUpdate` event which is immediately UPSERTed into PostgreSQL.

```
Alpaca TradingStream (WebSocket)
    └── TradeUpdate events
            └── UPSERT → orders table
```

Order lifecycle captured:

```
NEW → PENDING_NEW → PARTIAL_FILL → FILLED
                              └──→ CANCELED / EXPIRED
```

On startup, the app reconciles against `TradingClient.get_orders()` (REST) to backfill any events missed while the service was down. The UPSERT is idempotent — replaying events is safe.

### `price_alerts` — user-defined trigger rules

Managed via the app's own REST endpoints. A price alert is a threshold rule tied to a symbol (e.g., "alert me when AAPL drops below $193"). It has a natural lifecycle that produces all three CDC event types:

```
POST   /alerts              →  INSERT   (status: active)
                               alert fires when price crosses threshold
PATCH  /alerts/{id}         →  UPDATE   (status: active → triggered)
DELETE /alerts/{id}         →  DELETE
```

Alert checking is driven by `StockDataStream`. The app subscribes to a symbol's real-time quotes when an alert is created for it and unsubscribes when the last alert for that symbol is removed or triggered.

```
POST /alerts (AAPL, threshold=193, below)
    └── subscribe to AAPL quotes in StockDataStream

AAPL quote arrives (price=192.80)
    └── threshold crossed
            └── UPDATE price_alerts SET status='triggered'
                    └── Debezium captures before/after diff → Kafka
```

### Startup sequence

Order matters — symbols must exist before orders or alerts can reference them:

```
1. sync_symbols()        — load reference data from Alpaca REST
2. reconcile_orders()    — backfill missed orders via TradingClient REST
3. start TradingStream   — go live on real-time order updates
4. start FastAPI         — accept price alert CRUD requests
5. start StockDataStream — subscribe to symbols with active alerts
```

---

## Component 2 — Alpaca Market Data Stream (Streaming Ingestion)

A separate ingestion service that connects to Alpaca's `StockDataStream` WebSocket and produces market trade ticks directly to Kafka — PostgreSQL is not involved.

```
Alpaca StockDataStream (WebSocket)  →  Kafka producer  →  stock.public.trades
```

Trades are immutable facts — they are never updated or deleted — so CDC adds no value and only increases latency. Direct streaming is the right path here.

---

## Ingestion Architecture

Two paths, chosen based on data mutability:

### CDC path — Alpaca Custom Price Alert app → PostgreSQL → Debezium → Kafka

Used for data that **mutates**: orders, symbols, price alerts.

```
Alpaca Custom Price Alert app  →  PostgreSQL  →  WAL  →  Debezium  →  Kafka
```

PostgreSQL is the operational source of truth. Debezium reads the WAL via a replication slot and emits every INSERT, UPDATE, and DELETE as a change event into Kafka. Because Debezium tracks its WAL offset (LSN), it resumes exactly where it left off if Kafka goes down — no events are lost as long as the replication slot exists.

### Streaming path — Alpaca Market Data WebSocket → Kafka

Used for data that is **insert-only and high volume**: market trade ticks.

```
Alpaca StockDataStream  →  Kafka producer  →  Kafka
```

If this service goes down, ticks during the gap are lost. Recovery is via `StockHistoricalDataClient` (Alpaca's historical REST API) — detect the last ingested timestamp, fetch the gap, and re-produce to Kafka.

### Why the split

| | CDC path | Streaming path |
|---|---|---|
| Data | orders, symbols, price alerts | market trade ticks |
| Mutation | INSERT + UPDATE + DELETE | INSERT only |
| Volume | Low–medium | High |
| Durability buffer | PostgreSQL WAL + replication slot | Kafka producer retries |
| Downtime recovery | Debezium replays from LSN automatically | Backfill via historical REST API |
| Failure isolation | Debezium can lag; ticks still flow | Order data safe in Postgres if Kafka is down |

---

## Serving Layers

### Operational — Alpaca Custom Price Alert API (PostgreSQL)

The same FastAPI app that writes to PostgreSQL also serves current-state operational queries directly from it — no ClickHouse involved.

| Endpoint | Description |
|----------|-------------|
| `GET /symbols` | List tradeable symbols |
| `GET /orders` | Current order positions and status |
| `POST /alerts` | Create a new price alert |
| `GET /alerts` | List all active alerts |
| `PATCH /alerts/{id}` | Update alert threshold |
| `DELETE /alerts/{id}` | Remove an alert |

### Analytical — AI Chat Interface (ClickHouse)

An AI chat interface that allows users to ask natural language questions about their trading history and get insights from ClickHouse. The LLM translates the question to SQL, runs it against ClickHouse, and returns a human-readable answer.

Example questions:

- *"How much slippage did I have on AAPL last week?"*
- *"Which of my alerts were predictive vs noise?"*
- *"What was the market doing when I got filled on MSFT?"*
- *"Which symbols had the best P&L this month?"*
- *"Did I tend to enter at the top of spikes or during dips?"*

The split between serving layers follows query type:

| Query type | Source | Why |
|--|--|--|
| What are my open orders? | PostgreSQL (operational app) | Current state, strong consistency |
| How did my strategy perform last month? | ClickHouse (AI chat) | Historical aggregation, columnar is fast |
| Was my alert threshold well-calibrated? | ClickHouse (AI chat) | Joins across orders + trades + alerts over time |

---

## Core Business Questions

### 1. Slippage — did I get a good fill?

```
orders.filled_avg_price  vs  trades WHERE symbol matches AND trade_ts ≈ orders.filled_at
```

### 2. Execution timing — did I enter at the right moment?

```
orders.submitted_at  →  1-minute OHLCV bar from trades
```

### 3. Alert effectiveness — are my triggers well-calibrated?

```
price_alerts  →  trades WHERE trade_ts > triggered_at  (next N minutes)
```

### 4. Symbol-level P&L — which plays performed?

```
orders WHERE status = 'filled'  →  GROUP BY symbol  →  buy_avg, sell_avg, net
```

### 5. Market context at fill time — what was the market doing when I traded?

Join filled orders against OHLCV bars to see if fills happened during trending or ranging conditions.

---

## Kafka Topic Design

| Topic | Source | Partitions | Ingestion method |
|-------|--------|------------|------------------|
| `stock.public.trades` | Alpaca market data stream | 6 | Direct streaming |
| `stock.public.orders` | Alpaca Custom Price Alert app | 3 | CDC |
| `stock.public.symbols` | Alpaca Custom Price Alert app | 1 | CDC |
| `stock.public.price_alerts` | Alpaca Custom Price Alert app | 1 | CDC |

Trades get the most partitions because they are the highest volume and benefit most from parallel consumption into ClickHouse.

---

## Analytical Store (ClickHouse)

ClickHouse is the data warehouse for all historical analysis. Data lands here from Kafka via the native Kafka engine and materialized views.

The `ohlcv_1m` materialized view pre-aggregates trades into 1-minute OHLCV bars in real time — the primary structure used to answer execution timing and alert effectiveness questions.

---

## End-to-End Data Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                          SOURCE LAYER                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │          Alpaca Custom Price Alert (FastAPI app)          │   │
│  │                                                          │   │
│  │  Alpaca REST (symbols)    ──────────────────────────┐   │   │
│  │  Alpaca TradingStream (orders) ────────────────┐    │   │   │
│  │  Price Alert CRUD (/alerts) ───────────────┐   │    │   │   │
│  │  StockDataStream (alert checks) ───────┐   │   │    │   │   │
│  │                                        ▼   ▼   ▼    ▼   │   │
│  │                                      PostgreSQL          │   │
│  │                                          │               │   │
│  │                              WAL → Debezium              │   │
│  │                                          │               │   │
│  │                    GET /symbols          ▼               │   │
│  │                    GET /orders    Kafka (orders,         │   │
│  │                    GET /alerts           symbols,        │   │
│  │                    POST /alerts          price_alerts)   │   │
│  │                    PATCH /alerts/{id}                    │   │
│  │                    DELETE /alerts/{id}                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │        Alpaca Market Data Stream (ingestion service)      │   │
│  │                                                          │   │
│  │  StockDataStream WebSocket  ──►  Kafka producer          │   │
│  │                                          │               │   │
│  │                                          ▼               │   │
│  │                                   Kafka (trades)         │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────▼──────────────────┐
          │            TRANSPORT LAYER            │
          │      Kafka (KRaft, no Zookeeper)      │
          └───────────────────┬──────────────────┘
                              │
          ┌───────────────────▼──────────────────┐
          │           ANALYTICAL STORE            │
          │  ClickHouse                           │
          │  ├── trades (MergeTree)               │
          │  ├── orders (ReplacingMergeTree)      │
          │  ├── symbols (ReplacingMergeTree)     │
          │  ├── price_alerts (ReplacingMergeTree)│
          │  └── ohlcv_1m (AggregatingMV)        │
          └───────────────────┬──────────────────┘
                              │
          ┌───────────────────▼──────────────────┐
          │          SERVING LAYER               │
          │       AI Chat Interface              │
          │                                      │
          │   natural language question          │
          │         │                            │
          │         ▼                            │
          │   LLM → SQL → ClickHouse             │
          │         │                            │
          │         ▼                            │
          │   human-readable insight             │
          └──────────────────────────────────────┘
```
