---
trigger: model_decision
description: Use when designing or reviewing REST HTTP APIs or Python library APIs, including naming endpoints or functions, structuring requests and responses, handling errors, and designing authentication.
---

# API Design

Good APIs are easy to use correctly and hard to use incorrectly. A caller should rarely need to read the implementation.

---

## REST APIs

### Naming
- Resources are **nouns, plural**: `/users`, `/orders/{id}/items`
- Actions are **HTTP verbs**, not URL verbs: `POST /users` not `POST /createUser`
- Use **kebab-case** for multi-word segments: `/payment-methods`
- Nest only one level deep: `/users/{id}/orders`, not `/users/{id}/orders/{id}/items/{id}`

### Request / Response Structure
- Return consistent envelope or no envelope — never mix
- Use **camelCase** for JSON fields (or snake_case — pick one, never both)
- Always include `id`, `created_at`, `updated_at` on persisted resources
- Paginated lists: return `{ data: [...], total, page, per_page }`
- Never return a bare array as the top-level response (hard to extend later)

```json
// ❌
[{ "id": 1, "name": "Alice" }]

// ✅
{ "data": [{ "id": 1, "name": "Alice" }], "total": 1, "page": 1, "per_page": 20 }
```

### Error Handling
Use standard HTTP status codes consistently:

| Situation | Code |
|---|---|
| Bad input from caller | `400 Bad Request` |
| Missing or invalid auth | `401 Unauthorized` |
| Valid auth, insufficient permission | `403 Forbidden` |
| Resource not found | `404 Not Found` |
| Conflict (duplicate, stale write) | `409 Conflict` |
| Server fault | `500 Internal Server Error` |

Always return a structured error body — never a bare string:
```json
{ "error": "validation_failed", "message": "Email is required", "field": "email" }
```

### Authentication
- Use **Bearer tokens** in `Authorization` header, not query params
- Prefer **short-lived JWTs + refresh tokens** over long-lived API keys for user-facing APIs
- For server-to-server: static API keys in `Authorization: Bearer <key>` are fine, rotate them
- Never put secrets in URLs — they appear in logs

---

## Python Library APIs

### Naming
- Functions: verb phrases — `get_user()`, `create_order()`, `validate_email()`
- Booleans: `is_`, `has_`, `can_` prefix — `is_active`, `has_permission`
- Avoid vague names: `process_`, `handle_`, `do_` — name what it actually does

### Signatures
- Keyword-only args for anything optional or easily confused: `def send(*, to, subject, body, cc=None)`
- `@dataclass` when 4+ related args travel together
- Never mutable defaults — use `None` and init inside
- Return `None` explicitly or raise — don't return `False` as an error signal

### Error Handling
- Raise specific exceptions, not generic `Exception` or bare strings
- Create a small exception hierarchy for your library:
```python
class LibraryError(Exception): ...
class NotFoundError(LibraryError): ...
class ValidationError(LibraryError): ...
```
- Document what each public function can raise

### Response / Return Structure
- Return `@dataclass` or `NamedTuple` instead of raw dicts or tuples for structured data
- Functions that can fail: raise an exception — don't return `(result, error)` tuples
- Predicates return `bool`, not truthy values

---

## Quick Reference

| Problem | Fix |
|---|---|
| Verb in REST URL | Use HTTP method instead |
| Bare array response | Wrap in `{ data: [...] }` |
| Inconsistent error shape | Structured `{ error, message }` always |
| Wrong status code | 400 bad input, 401 no auth, 403 no permission, 404 missing |
| Secret in URL | Move to `Authorization` header |
| Vague function name | Rename to what it actually does |
| Too many positional args | Keyword-only + `@dataclass` |
| Dict/tuple return | `NamedTuple` or `@dataclass` |
| `(result, error)` return | Raise exceptions instead |