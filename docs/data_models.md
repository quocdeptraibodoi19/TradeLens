# Data Models — Operational Database (PostgreSQL)

## Entity Relationship Diagram

```mermaid
erDiagram
    symbols {
        uuid        id                              PK
        string      symbol                          UK
        string      name
        string      asset_class
        string      exchange
        string      status
        boolean     tradable
        boolean     marginable
        numeric     maintenance_margin_requirement
        string      margin_requirement_long
        string      margin_requirement_short
        boolean     shortable
        boolean     easy_to_borrow
        boolean     fractionable
        string[]    attributes
    }

    orders {
        uuid        id                  PK
        uuid        client_order_id
        uuid        asset_id
        string      symbol              FK
        string      asset_class
        string      side
        string      order_type
        string      time_in_force
        boolean     extended_hours
        numeric     qty
        numeric     notional
        numeric     limit_price
        numeric     stop_price
        numeric     trail_price
        numeric     trail_percent
        numeric     filled_qty
        numeric     filled_avg_price
        string      status
        timestamptz created_at
        timestamptz updated_at
        timestamptz submitted_at
        timestamptz filled_at
        timestamptz canceled_at
        timestamptz expired_at
        timestamptz failed_at
        timestamptz replaced_at
        uuid        replaced_by
        uuid        replaces
        timestamptz expires_at
    }

    price_alerts {
        uuid        id
        string      symbol              FK
        string      condition
        numeric     threshold
        string      status
        timestamptz created_at
        timestamptz triggered_at
    }

    symbols ||--o{ orders : "symbol"
    symbols ||--o{ price_alerts : "symbol"
```

## Relationships

| From | To | Cardinality | Description |
|---|---|---|---|
| `symbols` | `orders` | one-to-many | Each order references one tradeable symbol |
| `symbols` | `price_alerts` | one-to-many | Each alert is tied to one symbol's price feed |

## Notes

- `orders` and `price_alerts` are **not directly related** — they join analytically via `symbol` and timestamps in ClickHouse
- `symbols.symbol` is the FK target (not `id`) because it is the natural join key used across the pipeline
- `orders.qty` and `orders.notional` are mutually exclusive — dollar-based orders set `notional`, share-based orders set `qty`
- `orders.replaced_by` and `orders.replaces` are self-referencing UUIDs for order amendment tracking
