# Mailer Agent — Implementation Taskboard

> Long-term, iterative implementation plan. Each phase is a set of feature branches merged to `dev`.
> Follows: `feature/name` → `dev` → `staging` → `main` (per `git-basics` skill).
> Worktrees used for isolation (per `worktrees` skill).

---

## Branch & Workflow Rules

- **Branch from:** `dev` (always)
- **Branch naming:** `feature/<phase>-<short-name>` (e.g., `feature/p1-db-schema`)
- **Commits:** atomic, conventional (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`)
- **Merge:** PR into `dev`, keep branch after merge
- **Worktrees:** each feature branch gets its own worktree via `.worktrees/`
- **Testing:** every branch must pass tests before merge

---

## Phase 0: Project Bootstrap

### `feature/p0-project-init`
- [ ] Initialize git, create `dev` branch, push initial commit (docs only)
- [ ] Set up `.gitignore` (Python, Node, env, `.worktrees/`)
- [ ] Create `pyproject.toml` with project metadata and dependencies
- [ ] Set up FastAPI project structure: `server/main.py`, `server/__init__.py`
- [ ] Add `alembic` for migrations: `alembic init server/migrations`
- [ ] Add basic `docker-compose.yml` with PostgreSQL service
- [ ] Add `scripts/dev.sh` (start server + DB)
- [ ] Verify: `uvicorn server.main:app` starts, health endpoint returns 200

### `feature/p0-frontend-init`
- [ ] Initialize Next.js app in `app/`
- [ ] Set up design system: CSS variables from `04-frontend-design.md` (colors, typography, spacing)
- [ ] Create app shell layout: `Navbar`, `Sidebar`, main content area
- [ ] Add `Inter` and `JetBrains Mono` fonts
- [ ] Verify: `npm run dev` renders app shell

---

## Phase 1: Database & Models

### `feature/p1-db-enums-and-users`
- [ ] Create enum types: `global_role_enum`, `group_role_enum`, `auth_provider_enum`, `mail_status_enum`, `notification_type_enum`
- [ ] Create `users` table with all auth fields (`password_hash`, `provider`, `google_id`, `email_verified`)
- [ ] Create `email_verifications` table
- [ ] Add `update_updated_at()` trigger function
- [ ] Write SQLAlchemy models for `User`, `EmailVerification`
- [ ] Create alembic migration
- [ ] Verify: migration runs against Docker Postgres, tables created

### `feature/p1-groups-and-membership`
- [ ] Create `groups` table
- [ ] Create `user_groups` join table with `group_role_enum`
- [ ] Write SQLAlchemy models for `Group`, `UserGroup`
- [ ] Create alembic migration
- [ ] Verify: migration runs, FK constraints hold

### `feature/p1-templates`
- [ ] Create `templates` table with JSONB `fields`
- [ ] Create `group_templates` join table
- [ ] Write SQLAlchemy models for `Template`, `GroupTemplate`
- [ ] Create alembic migration
- [ ] Verify: can insert template with JSONB fields

### `feature/p1-mails-and-notifications`
- [ ] Create `mails` table with `body_original`, `body_final`, `field_values`
- [ ] Create `mail_recipients` table (FK to `users`)
- [ ] Create `notifications` table with partial index on unread
- [ ] Create `smtp_credentials` table
- [ ] Write SQLAlchemy models for `Mail`, `MailRecipient`, `Notification`, `SmtpCredential`
- [ ] Create alembic migration
- [ ] Verify: full schema matches `01-database-schema.md`

---

## Phase 2: Authentication

### `feature/p2-email-auth`
- [ ] Create Pydantic schemas: `RegisterRequest`, `LoginRequest`, `TokenResponse`
- [ ] Implement `POST /auth/register` — bcrypt hash, insert user, send verification email
- [ ] Implement `POST /auth/login` — verify credentials, return JWT
- [ ] Implement `POST /auth/verify-email` — consume token, set `email_verified`
- [ ] Implement `POST /auth/resend-verification`
- [ ] Add `get_current_user` dependency (JWT → User)
- [ ] Add `require_verified_email` dependency
- [ ] Tests: register, login, verify email, reject unverified, invalid token
- [ ] Verify: full email auth flow works end-to-end

### `feature/p2-google-oauth`
- [ ] Implement `GET /auth/google` — redirect to Google consent
- [ ] Implement `GET /auth/google/callback` — exchange code, create/link user, return JWT
- [ ] Implement `POST /auth/link-google` — link Google to existing email account
- [ ] Handle: new user, existing email (link), existing google_id (login)
- [ ] Tests: OAuth flow, account linking, email mismatch rejection
- [ ] Verify: Google OAuth login creates user with `email_verified=true`

### `feature/p2-role-dependencies`
- [ ] Implement `require_global_role(min_role)` dependency
- [ ] Implement `require_group_role(min_role)` dependency with effective role computation
- [ ] Implement `effective_group_role()` helper — `MAX(global, group)`
- [ ] Tests: role hierarchy, global floor behavior, non-member rejection
- [ ] Verify: role checks work for all combinations

### `feature/p2-frontend-auth`
- [ ] Build auth page (`/auth`) — login/register tabs, Google button
- [ ] Implement JWT storage and `Authorization` header injection
- [ ] Add protected route wrapper (redirect to `/auth` if no token)
- [ ] Add email verification banner
- [ ] Verify: login, register, Google OAuth redirect, protected routes

---

## Phase 3: Users & Groups

### `feature/p3-users-api`
- [ ] Implement `GET /users/me` — current user profile
- [ ] Implement `PATCH /users/me` — update name, avatar
- [ ] Implement `GET /users` — admin-only user list with search/pagination
- [ ] Implement `PATCH /users/{id}/role` — role assignment with constraints
- [ ] Tests: profile CRUD, role assignment rules, pagination
- [ ] Verify: admin can list users, assign roles within constraints

### `feature/p3-groups-api`
- [ ] Implement `POST /groups` — admin creates group, auto-added as owner
- [ ] Implement `GET /groups` — user sees own groups, admin sees all
- [ ] Implement `GET /groups/{id}`, `PATCH /groups/{id}`, `DELETE /groups/{id}`
- [ ] Tests: group CRUD, visibility rules, role-based access
- [ ] Verify: users only see their groups, admins see all

### `feature/p3-group-members-api`
- [ ] Implement `GET /groups/{id}/members` — list members with effective role
- [ ] Implement `POST /groups/{id}/members` — add user to group
- [ ] Implement `PATCH /groups/{id}/members/{user_id}` — change group role
- [ ] Implement `DELETE /groups/{id}/members/{user_id}` — remove member
- [ ] Tests: member CRUD, role constraints, effective role computation
- [ ] Verify: correct effective roles displayed

### `feature/p3-frontend-dashboard`
- [ ] Build dashboard page (`/dashboard`) — group cards grid
- [ ] Implement group card component (name, description, counts, role badge)
- [ ] Add "My Groups" / "All Groups" toggle for admins
- [ ] Add "Create Group" button + modal (admin+)
- [ ] Build empty state
- [ ] Verify: dashboard loads groups, cards display correctly

### `feature/p3-frontend-group-page`
- [ ] Build group page layout (`/groups/[groupId]`) with sidebar
- [ ] Build members sub-page — table, search, add/remove
- [ ] Add role dropdown per member (admin+)
- [ ] Build settings sub-page (admin+) — group info edit, danger zone
- [ ] Verify: group navigation, member management works

---

## Phase 4: Templates

### `feature/p4-templates-api`
- [ ] Implement `POST /templates` — create template
- [ ] Implement `GET /templates` — list accessible templates with filters
- [ ] Implement `GET /templates/{id}`, `PATCH /templates/{id}`, `DELETE /templates/{id}`
- [ ] Implement `POST /groups/{id}/templates` — add template to group (visibility rules)
- [ ] Implement `DELETE /groups/{id}/templates/{id}` — remove from group
- [ ] Tests: CRUD, visibility rules, moderator vs admin template access
- [ ] Verify: moderators add own templates, admins add any

### `feature/p4-template-generation`
- [ ] Implement `POST /templates/generate` — LLM-based template creation
- [ ] First call: send description, return MCQ refinement questions
- [ ] Second call: send description + answers, return finalized template
- [ ] Tests: prompt construction, response parsing
- [ ] Verify: LLM returns valid template structure

### `feature/p4-frontend-templates`
- [ ] Build templates sub-page in group view — template cards grid
- [ ] Build "Add Existing Template" modal with "My/All" toggle
- [ ] Build template creation page (`/templates/new`) — 3-step wizard
- [ ] Verify: template creation, linking to groups, visibility

---

## Phase 5: Mails (Core Feature)

### `feature/p5-mail-draft-api`
- [ ] Implement `POST /groups/{id}/mails/draft` — LLM generates draft
- [ ] Construct prompt from template + field values + additional info
- [ ] Store `body_original = body_final = LLM output`
- [ ] Store `field_values` snapshot and recipients
- [ ] Implement `GET /groups/{id}/mails` — list with status filter
- [ ] Implement `GET /groups/{id}/mails/{id}` — detail with diff data
- [ ] Implement `PATCH /groups/{id}/mails/{id}` — edit body_final (draft/rejected only)
- [ ] Implement `POST /groups/{id}/mails/{id}/regenerate` — re-call LLM, reset body_final
- [ ] Tests: draft creation, LLM prompt construction, edit restrictions
- [ ] Verify: draft created, body_original preserved on edit

### `feature/p5-approval-flow-api`
- [ ] Implement `POST .../mails/{id}/submit` — status → pending_approval
- [ ] Implement `POST .../mails/{id}/approve` — status → approved, optional body edit
- [ ] Implement `POST .../mails/{id}/reject` — status → rejected with reason
- [ ] Trigger notifications on each state change
- [ ] Tests: state transitions, role checks, creator-cannot-approve, rejection reason
- [ ] Verify: full approval lifecycle works

### `feature/p5-smtp-send`
- [ ] Implement `PUT /groups/{id}/smtp` — set encrypted SMTP credentials
- [ ] Implement `GET /groups/{id}/smtp` — check if configured (no password returned)
- [ ] Implement `DELETE /groups/{id}/smtp` — remove credentials
- [ ] Implement `GET /smtp/public-key` — return RSA public key
- [ ] Implement `POST .../mails/{id}/send` — decrypt, construct MIME, send via SMTP
- [ ] Error handling: missing credentials, auth failure, send failure
- [ ] Tests: SMTP config CRUD, send mock, error scenarios
- [ ] Verify: email actually sent via Gmail SMTP

### `feature/p5-frontend-mail-creation`
- [ ] Build mail creation page (`/groups/[groupId]/mails/new`)
- [ ] Phase 1: centered form (template select, dynamic fields, recipients chip-input)
- [ ] Phase 2: split-pane reveal animation (form slides left, editor fades in right)
- [ ] Integrate rich text editor (Tiptap or Lexical)
- [ ] Implement diff viewer (body_original vs body_final, toggle on/off)
- [ ] Add save draft, regenerate, submit actions
- [ ] Verify: full compose → edit → diff → submit flow

### `feature/p5-frontend-mail-review`
- [ ] Build mail detail/review page (`/groups/[groupId]/mails/[mailId]`)
- [ ] Read-only fields on left, editor with diff on right
- [ ] Approve/reject/send actions for moderator+
- [ ] Status timeline component
- [ ] Build mails sub-page in group view — table with status filters
- [ ] Verify: reviewer can see diffs, edit, approve, send

---

## Phase 6: Notifications

### `feature/p6-notifications-api`
- [ ] Implement `GET /notifications` — list with unread filter, pagination
- [ ] Implement `PATCH /notifications/{id}/read` — mark as read
- [ ] Implement `POST /notifications/read-all` — bulk mark read
- [ ] Tests: notification creation on events, read/unread queries
- [ ] Verify: notifications created on submit/approve/reject/send

### `feature/p6-frontend-notifications`
- [ ] Add notification bell in navbar with unread count badge
- [ ] Build notifications sub-page in group view
- [ ] Implement polling (30s interval)
- [ ] Click notification → navigate to related mail/group
- [ ] Add toast notifications for real-time feedback
- [ ] Verify: notifications appear, clicking navigates correctly

---

## Phase 7: SMTP Settings Frontend & Polish

### `feature/p7-smtp-frontend`
- [ ] Build SMTP config UI in group settings — email input, password input
- [ ] Client-side RSA encryption of app password before sending
- [ ] Fetch public key from `GET /smtp/public-key`
- [ ] Add "Test Connection" button
- [ ] Verify: credentials saved encrypted, mail sending works

### `feature/p7-polish`
- [ ] Add loading skeletons to all pages
- [ ] Add empty states to all list views
- [ ] Add error boundaries and error pages (404, 403, 500)
- [ ] Responsive testing: desktop, tablet, mobile
- [ ] Verify: all states handled gracefully

---

## Phase 8: Integration & Hardening

### `feature/p8-rate-limiting`
- [ ] Add rate limiting middleware (auth: 5/min/IP, LLM: 10/min/user)
- [ ] Tests: rate limit enforcement
- [ ] Verify: requests throttled correctly

### `feature/p8-cors-and-security`
- [ ] Configure CORS for frontend origin
- [ ] Add request ID middleware
- [ ] Add input validation review (Pydantic models at all boundaries)
- [ ] Verify: CORS headers, request IDs, validation rejections

### `feature/p8-docker-production`
- [ ] Create production `Dockerfile` for backend
- [ ] Create production `Dockerfile` for frontend
- [ ] Update `docker-compose.yml` with all services
- [ ] Add environment variable documentation
- [ ] Verify: full stack runs via `docker-compose up`

---

## Promotion Checkpoints

| Milestone | Merge to `staging` |
|---|---|
| Auth works (Phase 0–2 complete) | `dev → staging` — internal testing |
| Groups + Templates (Phase 3–4 complete) | `dev → staging` — feature review |
| Full mail flow (Phase 5–6 complete) | `dev → staging` — user acceptance testing |
| Production ready (Phase 7–8 complete) | `staging → main` — tag `v1.0.0` |
