---
trigger: always_on
---

# Engineering Guidelines

These apply to every task, always.

---

## Code

- **YAGNI** — build what's needed now, not what might be needed later
- **KISS** — the simplest solution that works is the right one
- **DRY** — one source of truth; duplication is a liability, not convenience
- **Names over comments** — rename until the code explains itself; comments explain *why*, never *what*
- **Small units** — functions do one thing; if you can say "and", split it
- **Fail loudly** — raise specific exceptions, never silently swallow errors or return ambiguous values
- **No magic values** — named constants or enums, never bare strings or numbers in logic

## Design

- **Separate concerns** — I/O, logic, and persistence belong in different layers
- **Dependencies flow inward** — outer layers (routes, CLI) depend on inner (services, domain); never the reverse
- **Prefer composition over inheritance** — inherit only when the relationship is truly "is-a"
- **Design for deletion** — if a module is hard to remove, it's too coupled

## Iteration

- **Make it work → make it right → make it fast** — in that order, never skip ahead
- **Small commits, one concern each** — a commit that does two things should be two commits
- **Refactor under green tests** — never refactor and add features in the same change
- **Leave it better than you found it** — every touch is an opportunity for small improvement

## Testing

- **Test behaviour, not implementation** — tests should survive refactors
- **One assertion of intent per test** — tests that check many things hide which thing broke
- **Tests are documentation** — test names should read like specs: `test_user_cannot_login_with_wrong_password`
- **If it's hard to test, the design is wrong** — untestable code is a design signal, not a test problem

## Safety

- **Validate at boundaries** — sanitize and type-check all input at the entry point; trust it inside
- **Least privilege** — code, DB users, and API keys should access only what they need
- **Secrets never in code** — env vars or secret managers only; never committed to source control
- **Destructive operations are irreversible** — confirm, back up, and migrate data before dropping or overwriting

---

*When in doubt: the next developer to read this is you in six months. Write for them.*