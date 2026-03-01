---
trigger: model_decision
description: Use when building or reviewing FastAPI applications, including route design, dependency injection, Pydantic validation, middleware, async patterns, database sessions, background tasks, and worker pool architecture.
---

# FastAPI Design

Routes should be thin dispatchers. Business logic lives in services, not in route handlers.

---

## Project Structure

```
app/
  api/
    routes/         # thin route handlers only
    dependencies/   # reusable Depends()
  services/         # business logic
  models/           # SQLAlchemy / ORM models
  schemas/          # Pydantic input/output schemas
  core/
    config.py       # settings via pydantic-settings
    middleware.py
  workers/          # background/worker logic
  tests/
```

---

## Thin Routes

Routes own: auth, request parsing, response shaping. Nothing else.

```python
# ❌ Fat route — logic leaks in
@router.post("/users")
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email taken")
    user = User(**data.model_dump())
    db.add(user); db.commit(); db.refresh(user)
    return user

# ✅ Thin route — delegates to service
@router.post("/users", response_model=UserOut, status_code=201)
async def create_user(data: UserCreate, svc: UserService = Depends(get_user_service)):
    return await svc.create(data)
```

---

## Pydantic Schemas

- Separate schemas for input (`UserCreate`), output (`UserOut`), and internal updates (`UserUpdate`)
- Never reuse ORM models as response schemas
- Use `model_config = ConfigDict(from_attributes=True)` on output schemas
- Validate at the boundary — services receive clean, typed data

```python
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    role: Literal["admin", "user"] = "user"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    model_config = ConfigDict(from_attributes=True)
```

---

## Dependency Injection

Use `Depends()` for anything shared or swappable: db sessions, current user, services, config.

```python
# DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Current user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    return await auth_service.verify_token(token, db)

# Service wired with its deps
def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)
```

Nest dependencies freely — FastAPI caches them per request. Avoid global state.

---

## Database Session Management

- Use `AsyncSession` + `async with` — never sync sessions in async routes
- One session per request via `Depends(get_db)`, not per operation
- Commit in the service layer, not the route
- Use `expire_on_commit=False` to avoid lazy-load errors after commit

```python
class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserCreate) -> User:
        if await self.db.scalar(select(User).where(User.email == data.email)):
            raise ValueError("Email already taken")
        user = User(**data.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
```

---

## Async / Await

- All route handlers should be `async def` — sync handlers block the event loop
- Use `await` for all I/O: DB queries, HTTP calls, file reads
- CPU-bound work → `asyncio.run_in_executor()` or offload to a worker
- Never `time.sleep()` in async code — use `await asyncio.sleep()`

```python
# ❌ Blocks event loop
@router.get("/report")
def get_report():
    return heavy_computation()

# ✅ Offload CPU work
@router.get("/report")
async def get_report(executor: Executor = Depends(get_executor)):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, heavy_computation)
```

---

## Middleware

Register in `app/core/middleware.py`, add to app in `main.py`. Keep middleware stateless.

```python
# Timing + request ID — good middleware candidates
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

Use middleware for: logging, request IDs, timing, CORS, rate limiting.
Don't use middleware for: auth (use `Depends`), business logic, DB access.

---

## Background Tasks

Use FastAPI `BackgroundTasks` for fire-and-forget work that's fast and non-critical (email, logging). For reliable or heavy work, use a worker pool.

```python
@router.post("/users", status_code=201)
async def create_user(data: UserCreate, background_tasks: BackgroundTasks, svc: UserService = Depends(get_user_service)):
    user = await svc.create(data)
    background_tasks.add_task(send_welcome_email, user.email)
    return user
```

---

## Worker Pool Architecture

For CPU-bound, long-running, or reliable async work, decouple via a task queue.

```
FastAPI app  →  enqueue task  →  Queue (Redis / RabbitMQ)
                                      ↓
                              Worker pool (Celery / ARQ / dramatiq)
                                      ↓
                              DB / external services
```

- Workers run separately from the API process
- Tasks must be **idempotent** — retries happen
- Store task status in DB or cache if the caller needs to poll
- Expose task status via a `/tasks/{id}` endpoint

```python
# Enqueue (ARQ example)
@router.post("/reports")
async def generate_report(data: ReportRequest, redis=Depends(get_redis)):
    job = await redis.enqueue_job("generate_report_task", data.model_dump())
    return {"task_id": job.job_id}

# Worker
async def generate_report_task(ctx, data: dict):
    # runs in worker process, not in API
    ...
```

---

## Testing

Use `httpx.AsyncClient` with `app` directly — no running server needed.

```python
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

async def test_create_user(client):
    resp = await client.post("/users", json={"email": "a@b.com", "name": "Alice"})
    assert resp.status_code == 201
    assert resp.json()["email"] == "a@b.com"
```

- Override dependencies in tests with `app.dependency_overrides`
- Use a separate test DB, rolled back per test via transactions
- Test services independently from routes — services are plain Python classes

```python
app.dependency_overrides[get_db] = get_test_db
```

---

## Quick Reference

| Problem | Fix |
|---|---|
| Logic in route handler | Move to service |
| ORM model as response | Separate `Out` schema with `from_attributes=True` |
| Sync route in async app | `async def` + `await` all I/O |
| Global DB session | `Depends(get_db)` per request |
| Fire-and-forget task | `BackgroundTasks` |
| Heavy / reliable async work | Worker pool + task queue |
| Shared auth / config | Wire via `Depends()` |
| Middleware doing auth | Move to `Depends(get_current_user)` |
| Test hitting live server | `AsyncClient(app=app)` |
| Untestable route (fat deps) | `dependency_overrides` + thin services |