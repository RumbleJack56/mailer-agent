---
trigger: model_decision
description: Use when designing, reviewing, or modifying relational database schemas in PostgreSQL or MySQL, including table structure, normalization, naming, indexing, migrations, and long-term maintainability.
---

# Relational Database Design

A schema is the hardest thing to change later. Design it deliberately — mistakes compound as data accumulates.

**Core principle:** Design for reads. Normalize to eliminate inconsistency. Denormalize only when you can measure the need.

---

## Naming Conventions

Consistency matters more than which convention you pick. Pick one and never deviate.

- Tables: **snake_case, plural nouns** — `users`, `order_items`, `payment_methods`
- Columns: **snake_case** — `created_at`, `first_name`, `is_active`
- Primary keys: always `id` (not `user_id` on the `users` table)
- Foreign keys: `{referenced_table_singular}_id` — `user_id`, `order_id`
- Booleans: `is_`, `has_`, `can_` prefix — `is_active`, `has_verified_email`
- Timestamps: `_at` suffix — `created_at`, `updated_at`, `deleted_at`
- Junction tables: `{table_a}_{table_b}` alphabetically — `role_users`, `tag_posts`

---

## Schema Design Fundamentals

### Every table needs these columns
```sql
id          BIGSERIAL PRIMARY KEY,
created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
```
Use `BIGSERIAL` (not `SERIAL`) — you will exceed 2B rows eventually. Use `TIMESTAMPTZ` not `TIMESTAMP` — always store UTC.

### Use appropriate types
| Data | Type |
|---|---|
| Money / currency | `NUMERIC(12,2)`, never `FLOAT` |
| Status / state | `VARCHAR` with CHECK or a lookup table, not magic integers |
| Short text | `VARCHAR(n)` with a reasonable limit |
| Unlimited text | `TEXT` |
| Flags | `BOOLEAN NOT NULL DEFAULT false` |
| UUIDs | `UUID` (use when exposing IDs externally) |

### Constraints are documentation
Add them — they're enforced by the DB, not your application code:
```sql
email VARCHAR(255) NOT NULL UNIQUE,
status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'inactive', 'pending')),
price NUMERIC(10,2) NOT NULL CHECK (price >= 0)
```

---

## Normalization

Normalize to **3NF by default**. Denormalize only when a query is provably slow and normalization is the cause.

**1NF** — No repeating groups. Each cell holds one atomic value. No arrays of values in a column.
```sql
-- ❌ Repeating group
users: id, name, phone_1, phone_2, phone_3

-- ✅ Separate table
user_phones: id, user_id, phone, is_primary
```

**2NF** — Every non-key column depends on the whole primary key (matters for composite keys).
```sql
-- ❌ product_name depends only on product_id, not the full key (order_id, product_id)
order_items: order_id, product_id, product_name, quantity

-- ✅ product_name belongs on products
order_items: order_id, product_id, quantity
products: id, name, price
```

**3NF** — No transitive dependencies. Non-key columns depend only on the key, not on other non-key columns.
```sql
-- ❌ city depends on zip_code, not on user id
users: id, zip_code, city

-- ✅ Extract the dependency
zip_codes: zip_code, city
users: id, zip_code  -- FK to zip_codes
```

**When to denormalize:** Only when a join is the measured bottleneck. Keep the normalized source of truth — denormalize into a separate table or materialized view.

---

## Indexing Strategy

Indexes speed reads and slow writes. Add deliberately, not defensively. Always index: foreign keys (not automatic in Postgres/MySQL), columns in `WHERE`/`ORDER BY`/`JOIN` on large tables.

**Index types:**
```sql
-- Standard lookup
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Compound: put equality columns first, range columns last
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- Partial: index only the rows you query
CREATE INDEX idx_orders_pending ON orders(created_at) WHERE status = 'pending';

-- Unique constraint (also an index)
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

**Don't over-index:** Each index adds write overhead. Audit with `pg_stat_user_indexes` — unused indexes are pure cost.

---

## Schema Modification Guidelines

The schema outlasts any application version. Mistakes compound as data accumulates.

### Rules for safe migrations
1. **Never rename a column or table in one step** — deploy a new column, migrate data, then drop the old one over multiple releases
2. **Never add a NOT NULL column without a DEFAULT** — it locks the table during backfill on large datasets
3. **Never drop a column the application still reads** — remove application references first, then drop
4. **Always make migrations reversible** — write a `down` migration for every `up`
5. **One concern per migration** — never mix schema change + data backfill in one file

### Safe column addition
```sql
-- ✅ Safe: nullable first
ALTER TABLE users ADD COLUMN display_name VARCHAR(100);

-- Then backfill
UPDATE users SET display_name = first_name WHERE display_name IS NULL;

-- Then constrain (separate migration, after backfill is verified)
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;
```

### Destructive operations checklist
Before dropping a table, column, or index:
- [ ] Confirm no application code references it
- [ ] Confirm no queries in logs reference it
- [ ] Back up or archive if data has value
- [ ] Deploy removal in a separate release from the schema drop

---

## Designing for the Long Term

### Soft deletes
For records that should be recoverable or have referential history, use `deleted_at` instead of hard deletes:
```sql
deleted_at TIMESTAMPTZ DEFAULT NULL
```
Filter active records with `WHERE deleted_at IS NULL`. Add a partial index on it. Hard deletes are appropriate for ephemeral data (sessions, logs, caches).

### Audit trails
For regulated data or anything users dispute, track who changed what:
```sql
CREATE TABLE audit_log (
    id          BIGSERIAL PRIMARY KEY,
    table_name  VARCHAR(100) NOT NULL,
    record_id   BIGINT NOT NULL,
    action      VARCHAR(10) NOT NULL CHECK (action IN ('INSERT','UPDATE','DELETE')),
    changed_by  BIGINT REFERENCES users(id),
    changed_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    old_data    JSONB,
    new_data    JSONB
);
```

### Status columns over boolean flags
Booleans don't evolve gracefully. A status column does:
```sql
-- ❌ Adding a third state requires a new column
is_published BOOLEAN

-- ✅ New states are just new values
status VARCHAR(20) CHECK (status IN ('draft', 'published', 'archived'))
```

### Avoid EAV (Entity-Attribute-Value) tables
EAV (`id, entity_id, attribute_name, attribute_value`) feels flexible but destroys query performance, type safety, and constraint enforcement. Use `JSONB` for truly dynamic attributes instead:
```sql
metadata JSONB NOT NULL DEFAULT '{}'
```

---

## Quick Reference

| Problem | Fix |
|---|---|
| Repeating columns (`phone_1`, `phone_2`) | Separate child table |
| Storing money as FLOAT | `NUMERIC(12,2)` |
| Magic integer statuses | VARCHAR with CHECK constraint |
| Missing FK indexes | Index every foreign key |
| Over-indexing | Audit with `pg_stat_user_indexes` |
| Adding NOT NULL column to large table | Add nullable → backfill → constrain |
| Renaming a column live | Add new → migrate → drop old |
| Boolean that gained a third state | Replace with status VARCHAR |
| Dynamic attributes | `JSONB` column, not EAV table |
| No history on sensitive data | Audit log table |
| Hard deletes on important records | `deleted_at` soft delete |