---
trigger: model_decision
description: Use when code is hard to read, has grown complex over time, has duplicated logic, uses unclear variable names, has deeply nested conditions, or when asked to refactor, or simplify existing code. Also use before code review and/or feature addition.
---

# Python Code Simplification

Simplification reduces cognitive load — not just line count. Simple code is code a reader never has to think twice about.

## Checklist

### 1. Remove dead code
Unused imports, variables, parameters, commented-out blocks, unreachable branches. Use `ruff` to catch them automatically.

### 2. Rename for intent
Names should tell you *what*, not *how*. If you need to read the body to understand the name, rename it.
```python
# ❌
d, lst, flag = datetime.date.today(), [u for u in users if u.active], True
# ✅
today, active_users, has_results = ...
```
Avoid: single letters (except `i`/`j`), abbreviations (`usr`, `mgr`), negated booleans (`is_not_valid` → `is_invalid`), shadowing builtins (`list`, `id`, `type`).

### 3. Flatten control flow
Guard clauses first, happy path last. Replace manual loops with `any()`/`all()` and comprehensions when intent is clear.
```python
# ❌ Three levels deep
def process(order):
    if order:
        if order.is_valid():
            if order.user.is_active():
                return compute(order)

# ✅ Guards up front
def process(order):
    if not order or not order.is_valid() or not order.user.is_active():
        return None
    return compute(order)
```

### 4. Eliminate duplication
When the same structure appears 2+ times, extract it. Don't extract code that only *looks* similar but changes for different reasons.

### 5. Simplify function signatures
- 4+ positional args → group into a `@dataclass`
- Prevent silent ordering bugs → keyword-only args with `*`
- Boolean flag args → separate functions or `Enum`
- Never use mutable defaults → use `None` and init inside the body

```python
# ❌
def create_user(name, email, role, is_active, dept, manager_id): ...

# ✅
@dataclass
class UserConfig:
    name: str; email: str; role: str; dept: str; manager_id: int; is_active: bool = True

def create_user(config: UserConfig): ...
```

### 6. Single responsibility
If you describe a function with "and", split it. Signs: name has "and"/"also", >30 lines, hard to test without complex setup.

### 7. Simplify expressions
- Complex booleans → name the condition (`is_active_admin = ...`)
- Chained if/elif → `dict.get(key, default)`
- Magic values → named constants or `IntEnum`
- Structured return values → `NamedTuple` or `@dataclass` instead of raw tuples

## Quick Reference

| Problem | Fix |
|---|---|
| Deep nesting | Guard clauses |
| Vague names | Rename to intent |
| Duplicate logic | Extract shared function |
| Complex boolean | Name the condition |
| Chained if/elif | Dict lookup |
| Magic values | Named constant / `IntEnum` |
| Too many params | `@dataclass` + keyword-only |
| Boolean flag args | `Enum` or split function |
| Mutable defaults | Default `None`, init inside |
| Raw tuple returns | `NamedTuple` / `@dataclass` |