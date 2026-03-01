# API Design

> FastAPI REST API specification for the Mailer Agent application.
> All endpoints return JSON. Auth via JWT in `Authorization: Bearer <token>` header.

---

## 1. Base Configuration

| Property | Value |
|---|---|
| **Base URL** | `/api/v1` |
| **Content-Type** | `application/json` |
| **Auth** | JWT Bearer token (except auth endpoints) |
| **Error format** | `{ "detail": "message" }` |

**Standard HTTP status codes used:**

| Code | Meaning |
|---|---|
| `200` | Success |
| `201` | Created |
| `204` | No Content (successful delete) |
| `400` | Bad Request (validation error) |
| `401` | Unauthorized (missing/invalid token) |
| `403` | Forbidden (insufficient role) |
| `404` | Not Found |
| `409` | Conflict (duplicate resource) |
| `422` | Unprocessable Entity (schema validation) |

---

## 2. Authentication

### `POST /api/v1/auth/register`

Register a new user with email and password.

**Body:**
```json
{
  "email": "user@example.com",
  "name": "Jane Doe",
  "password": "secureP@ss123"
}
```

**Response `201`:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Jane Doe",
  "email_verified": false,
  "message": "Verification email sent"
}
```

> [!NOTE]
> Sends a verification email with a token link. User cannot perform protected actions until `email_verified = true`.

---

### `POST /api/v1/auth/login`

Login with email and password.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "secureP@ss123"
}
```

**Response `200`:**
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "Jane Doe",
    "global_role": "user",
    "email_verified": true
  }
}
```

**Error `401`:** Invalid credentials.
**Error `403`:** Email not verified.

---

### `GET /api/v1/auth/google`

Initiates Google OAuth flow. Redirects to Google consent screen.

**Query params:**
- `redirect_uri` (optional) — where to redirect after OAuth callback

---

### `GET /api/v1/auth/google/callback`

Google OAuth callback. Exchanges code for tokens, creates/links user.

**Query params:**
- `code` — authorization code from Google
- `state` — CSRF + redirect_uri encoded state

**Response `200`:** Same as login response (returns JWT).

> [!NOTE]
> If a user with the same email exists (registered via email), their `google_id` is linked automatically. They can now use either login method.

---

### `POST /api/v1/auth/verify-email`

Verify email address using the token from the verification link.

**Body:**
```json
{
  "token": "verification_token_string"
}
```

**Response `200`:**
```json
{
  "message": "Email verified successfully"
}
```

**Error `400`:** Token expired or already used.

---

### `POST /api/v1/auth/resend-verification`

Resend verification email. Requires valid JWT.

**Response `200`:**
```json
{
  "message": "Verification email sent"
}
```

---

### `POST /api/v1/auth/link-google`

Link Google account to an existing email-registered user. Requires valid JWT.

Initiates OAuth flow specifically for account linking.

---

## 3. Users

All endpoints require authentication.

### `GET /api/v1/users/me`

Get the current user's profile.

**Response `200`:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Jane Doe",
  "avatar_url": "https://...",
  "provider": "email",
  "google_id": "12345...",
  "email_verified": true,
  "global_role": "user",
  "is_active": true,
  "created_at": "2026-03-01T00:00:00Z"
}
```

---

### `PATCH /api/v1/users/me`

Update current user's profile (name, avatar).

**Body:**
```json
{
  "name": "New Name",
  "avatar_url": "https://..."
}
```

---

### `GET /api/v1/users`

List all users. **Requires:** `global_role >= admin`.

**Query params:**
- `search` — filter by name or email (partial match)
- `global_role` — filter by role
- `page`, `page_size` — pagination (default: 1, 20)

**Response `200`:**
```json
{
  "items": [ { "id": "...", "email": "...", "name": "...", "global_role": "..." } ],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

---

### `PATCH /api/v1/users/{user_id}/role`

Change a user's global role. **Requires:** `global_role >= admin` and target role < own role.

**Body:**
```json
{
  "global_role": "admin"
}
```

> [!IMPORTANT]
> **Role assignment constraints:**
> - `admin` can assign: `user`
> - `owner` can assign: `user`, `admin`
> - `root` can assign: `user`, `admin`, `owner`
> - No one can assign `root` (set via DB seed only)

---

## 4. Groups

### `POST /api/v1/groups`

Create a new group. **Requires:** `global_role >= admin`.

**Body:**
```json
{
  "name": "Marketing Team",
  "description": "Email templates for marketing campaigns"
}
```

**Response `201`:** Returns the created group. Creator is auto-added as `owner` in `user_groups`.

---

### `GET /api/v1/groups`

List groups visible to the current user.

- `global_role >= admin` → sees all groups
- `user` → sees only groups they belong to

**Query params:**
- `search` — filter by name
- `page`, `page_size`

---

### `GET /api/v1/groups/{group_id}`

Get group details. **Requires:** membership or `global_role >= admin`.

**Response `200`:**
```json
{
  "id": "uuid",
  "name": "Marketing Team",
  "description": "...",
  "created_by": "uuid",
  "member_count": 12,
  "template_count": 5,
  "created_at": "..."
}
```

---

### `PATCH /api/v1/groups/{group_id}`

Update group name/description. **Requires:** `effective_group_role >= admin`.

---

### `DELETE /api/v1/groups/{group_id}`

Delete a group. **Requires:** `effective_group_role >= owner`.

---

## 5. Group Members

### `GET /api/v1/groups/{group_id}/members`

List members of a group. **Requires:** membership or `global_role >= admin`.

**Response `200`:**
```json
{
  "items": [
    {
      "user_id": "uuid",
      "name": "Jane Doe",
      "email": "jane@example.com",
      "avatar_url": "...",
      "group_role": "moderator",
      "effective_role": "moderator",
      "joined_at": "..."
    }
  ],
  "total": 12
}
```

> [!NOTE]
> `effective_role` is computed as `MAX(user_groups.role, users.global_role)` and returned in the response for display.

---

### `POST /api/v1/groups/{group_id}/members`

Add a user to the group. **Requires:** `effective_group_role >= admin`.

**Body:**
```json
{
  "user_id": "uuid",
  "role": "user"
}
```

---

### `PATCH /api/v1/groups/{group_id}/members/{user_id}`

Change a member's group role. **Requires:** `effective_group_role >= admin` and target role < own role.

**Body:**
```json
{
  "role": "moderator"
}
```

---

### `DELETE /api/v1/groups/{group_id}/members/{user_id}`

Remove a member from the group. **Requires:** `effective_group_role >= admin`.

---

## 6. Templates

### `POST /api/v1/templates`

Create a new template. **Requires:** `effective_group_role >= moderator` in at least one group.

**Body:**
```json
{
  "name": "Meeting Follow-up",
  "description": "Post-meeting summary email",
  "prompt": "Write a follow-up email for {{meeting_topic}} discussed with {{attendees}}...",
  "fields": [
    { "key": "meeting_topic", "label": "Meeting Topic", "type": "text", "required": true },
    { "key": "attendees", "label": "Attendees", "type": "textarea", "required": true },
    { "key": "tone", "label": "Tone", "type": "select", "required": true, "options": ["formal", "casual"] }
  ]
}
```

**Response `201`:** Returns the created template.

---

### `GET /api/v1/templates`

List templates accessible to the current user (via group memberships).

**Query params:**
- `search` — filter by name
- `created_by` — `me` or `others` (for moderator filter)
- `group_id` — filter templates in a specific group
- `page`, `page_size`

---

### `GET /api/v1/templates/{template_id}`

Get template details. **Requires:** template is in a group the user belongs to, or `global_role >= admin`.

---

### `PATCH /api/v1/templates/{template_id}`

Update a template. **Requires:** creator of the template, or `global_role >= admin`.

---

### `DELETE /api/v1/templates/{template_id}`

Delete a template. **Requires:** creator of the template, or `global_role >= admin`.

---

### `POST /api/v1/groups/{group_id}/templates`

Add a template to a group. **Requires:** `effective_group_role >= moderator`.

**Body:**
```json
{
  "template_id": "uuid"
}
```

> [!IMPORTANT]
> **Visibility rules:**
> - Moderators can only add templates they created
> - Admins and above can add any template

---

### `DELETE /api/v1/groups/{group_id}/templates/{template_id}`

Remove a template from a group. **Requires:** `effective_group_role >= moderator`.

---

### `POST /api/v1/templates/generate`

AI-assisted template creation. Sends user input to LLM to generate a finalized template.

**Requires:** `effective_group_role >= moderator` in at least one group.

**Body:**
```json
{
  "description": "I need a template for sending project status updates to stakeholders",
  "answers": {
    "formality": "formal",
    "length": "medium",
    "includes_action_items": true
  }
}
```

**Response `200`:**
```json
{
  "name": "Project Status Update",
  "prompt": "Write a formal project status update...",
  "fields": [ { "key": "...", "label": "...", "type": "...", "required": true } ]
}
```

> User reviews, modifies, and then saves via `POST /api/v1/templates`.

---

## 7. Mails

### `POST /api/v1/groups/{group_id}/mails/draft`

Generate a mail draft from a template. Calls the LLM with prompt + filled fields.

**Requires:** membership in the group.

**Body:**
```json
{
  "template_id": "uuid",
  "field_values": {
    "meeting_topic": "Q1 Planning",
    "attendees": "John, Jane, Bob"
  },
  "additional_info": "Mention the budget deadline",
  "subject": "Follow-up: Q1 Planning Meeting",
  "recipients": [
    { "user_id": "uuid", "type": "to" },
    { "user_id": "uuid", "type": "cc" }
  ]
}
```

**Response `201`:**
```json
{
  "id": "uuid",
  "status": "draft",
  "subject": "Follow-up: Q1 Planning Meeting",
  "body_original": "Dear team, ...",
  "body_final": "Dear team, ...",
  "field_values": { "..." },
  "recipients": [ { "user_id": "...", "email": "...", "name": "...", "type": "to" } ],
  "created_at": "..."
}
```

---

### `GET /api/v1/groups/{group_id}/mails`

List mails in a group. **Requires:** membership.

**Query params:**
- `status` — filter by status (`draft`, `pending_approval`, `approved`, `rejected`, `sent`)
- `created_by` — filter by author (`me` or user_id)
- `page`, `page_size`

---

### `GET /api/v1/groups/{group_id}/mails/{mail_id}`

Get mail details including diff info. **Requires:** membership.

**Response `200`:**
```json
{
  "id": "uuid",
  "group_id": "uuid",
  "template": { "id": "uuid", "name": "Meeting Follow-up" },
  "created_by": { "id": "uuid", "name": "Jane Doe" },
  "approved_by": null,
  "subject": "...",
  "body_original": "LLM-generated text...",
  "body_final": "User-edited text...",
  "field_values": { "..." },
  "additional_info": "...",
  "recipients": [ { "user_id": "...", "email": "...", "name": "...", "type": "to" } ],
  "status": "draft",
  "approved_at": null,
  "sent_at": null,
  "created_at": "...",
  "updated_at": "..."
}
```

---

### `PATCH /api/v1/groups/{group_id}/mails/{mail_id}`

Update a mail draft (edit body, subject, recipients). **Requires:** creator of the mail, status = `draft` or `rejected`.

**Body:**
```json
{
  "subject": "Updated subject",
  "body_final": "Edited email body...",
  "recipients": [
    { "user_id": "uuid", "type": "to" }
  ]
}
```

---

### `POST /api/v1/groups/{group_id}/mails/{mail_id}/submit`

Submit mail for approval. Changes status `draft` → `pending_approval`.

**Requires:** creator of the mail.

> Triggers `approval_requested` notifications to all admins and moderators in the group.

---

### `POST /api/v1/groups/{group_id}/mails/{mail_id}/approve`

Approve a mail. Changes status `pending_approval` → `approved`.

**Requires:** `effective_group_role >= moderator`, not the creator.

**Body (optional):**
```json
{
  "body_final": "Optionally edited body by approver..."
}
```

> Triggers `mail_approved` notification to the creator.

---

### `POST /api/v1/groups/{group_id}/mails/{mail_id}/reject`

Reject a mail. Changes status `pending_approval` → `rejected`.

**Requires:** `effective_group_role >= moderator`.

**Body:**
```json
{
  "reason": "Please revise the second paragraph"
}
```

> Triggers `mail_rejected` notification to the creator.

---

### `POST /api/v1/groups/{group_id}/mails/{mail_id}/send`

Send an approved mail via SMTP. Changes status `approved` → `sent`.

**Requires:** `effective_group_role >= moderator`.

> Uses the group's SMTP credentials. Triggers `mail_sent` notification to the creator.

---

### `POST /api/v1/groups/{group_id}/mails/{mail_id}/regenerate`

Re-generate the LLM draft for a mail in `draft` or `rejected` status. Overwrites `body_original` and resets `body_final`.

**Requires:** creator of the mail.

---

## 8. Notifications

### `GET /api/v1/notifications`

List notifications for the current user.

**Query params:**
- `unread_only` — boolean, default `false`
- `page`, `page_size`

**Response `200`:**
```json
{
  "items": [
    {
      "id": "uuid",
      "type": "approval_requested",
      "title": "New mail awaiting approval",
      "message": "Jane submitted 'Q1 Follow-up' in Marketing Team",
      "mail_id": "uuid",
      "group_id": "uuid",
      "is_read": false,
      "created_at": "..."
    }
  ],
  "total": 5,
  "unread_count": 3
}
```

---

### `PATCH /api/v1/notifications/{notification_id}/read`

Mark a notification as read.

---

### `POST /api/v1/notifications/read-all`

Mark all notifications as read.

---

## 9. SMTP Credentials

### `PUT /api/v1/groups/{group_id}/smtp`

Set or update SMTP credentials for a group. **Requires:** `effective_group_role >= admin`.

**Body:**
```json
{
  "smtp_email": "team@gmail.com",
  "encrypted_app_password": "base64_rsa_encrypted_string"
}
```

---

### `GET /api/v1/groups/{group_id}/smtp`

Check if SMTP is configured (does not return the password). **Requires:** `effective_group_role >= admin`.

**Response `200`:**
```json
{
  "configured": true,
  "smtp_email": "team@gmail.com",
  "updated_at": "..."
}
```

---

### `DELETE /api/v1/groups/{group_id}/smtp`

Remove SMTP credentials. **Requires:** `effective_group_role >= admin`.

---

### `GET /api/v1/smtp/public-key`

Get the backend's RSA public key for encrypting app passwords client-side. **Public endpoint** (no auth required).

**Response `200`:**
```json
{
  "public_key": "-----BEGIN PUBLIC KEY-----\n..."
}
```

---

## 10. Dependency Injection & Middleware

### FastAPI Dependencies

| Dependency | Purpose |
|---|---|
| `get_current_user` | Extracts and validates JWT from `Authorization` header; returns `User` |
| `require_verified_email` | Chains on `get_current_user`, raises `403` if `email_verified = false` |
| `require_global_role(min_role)` | Checks `user.global_role >= min_role` |
| `require_group_role(min_role)` | Computes effective group role via `MAX(global, group)`, checks `>= min_role` |

### Middleware

| Middleware | Purpose |
|---|---|
| **CORS** | Allow Next.js frontend origin |
| **Request ID** | Attach UUID to each request for tracing |
| **Rate Limiting** | Per-user rate limits on auth and LLM endpoints |

---

## 11. Pagination Convention

All list endpoints use offset-based pagination:

```
?page=1&page_size=20
```

**Response envelope:**
```json
{
  "items": [],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```
