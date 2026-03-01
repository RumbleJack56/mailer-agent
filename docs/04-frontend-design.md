# Frontend Design

> Next.js frontend specification — pages, components, theme, and layout system.

---

## 1. Design System

### 1.1 Color Palette

The UI uses a **light theme** built around light blue, soft neutrals, and a warm yellow accent.

| Token | Swatch | Value | Usage |
|---|---|---|---|
| `--bg-primary` | ![](https://placehold.co/80x24/f2faff/f2faff) | `#f2faff` | Page background |
| `--bg-secondary` | ![](https://placehold.co/80x24/ffffff/ffffff) | `#ffffff` | Cards, panels |
| `--bg-tertiary` | ![](https://placehold.co/80x24/e8f4fd/e8f4fd) | `#e8f4fd` | Hover states, inputs |
| `--bg-elevated` | ![](https://placehold.co/80x24/ffffff/ffffff) | `#ffffff` | Modals, dropdowns |
| `--bg-highlight` | ![](https://placehold.co/80x24/eee8a9/eee8a9) | `#eee8a9` | Highlights, selected rows, callouts |
| `--text-primary` | ![](https://placehold.co/80x24/1a1a2e/1a1a2e) | `#1a1a2e` | Headings, body |
| `--text-secondary` | ![](https://placehold.co/80x24/5a6478/5a6478) | `#5a6478` | Labels, captions |
| `--text-muted` | ![](https://placehold.co/80x24/9ca3af/9ca3af) | `#9ca3af` | Placeholders, disabled |
| `--border` | ![](https://placehold.co/80x24/d6e4ef/d6e4ef) | `#d6e4ef` | Dividers, card borders |
| `--border-focus` | ![](https://placehold.co/80x24/46a6ff/46a6ff) | `#46a6ff` | Focused inputs |
| `--accent` | ![](https://placehold.co/80x24/46a6ff/46a6ff) | `#46a6ff` | Primary buttons, links, active states |
| `--accent-hover` | ![](https://placehold.co/80x24/2e8fe6/2e8fe6) | `#2e8fe6` | Button hover (darker) |
| `--accent-muted` | ![](https://placehold.co/80x24/7592bc/7592bc) | `#7592bc` | Secondary buttons, inactive tabs, subtle accents |
| `--accent-subtle` | ![](https://placehold.co/80x24/ddeeff/ddeeff) | `rgba(70,166,255,0.15)` | Active sidebar item, selected row bg |
| `--success` | ![](https://placehold.co/80x24/22c55e/22c55e) | `#22c55e` | Approved, sent badges |
| `--warning` | ![](https://placehold.co/80x24/eee8a9/eee8a9) | `#eee8a9` | Pending approval badges |
| `--warning-text` | ![](https://placehold.co/80x24/92860a/92860a) | `#92860a` | Warning text on yellow bg |
| `--danger` | ![](https://placehold.co/80x24/ef4444/ef4444) | `#ef4444` | Rejected, errors |
| `--info` | ![](https://placehold.co/80x24/7592bc/7592bc) | `#7592bc` | Info badges, notifications |
| `--neutral-50` | ![](https://placehold.co/80x24/f9fafb/f9fafb) | `#f9fafb` | Subtle backgrounds |
| `--neutral-200` | ![](https://placehold.co/80x24/e5e7eb/e5e7eb) | `#e5e7eb` | Borders, dividers |
| `--neutral-500` | ![](https://placehold.co/80x24/6b7280/6b7280) | `#6b7280` | Secondary text |
| `--neutral-800` | ![](https://placehold.co/80x24/1f2937/1f2937) | `#1f2937` | Primary text |

### 1.2 Typography

| Element | Font | Size | Weight |
|---|---|---|---|
| Body | `Inter` | `14px` | 400 |
| Headings h1 | `Inter` | `28px` | 700 |
| Headings h2 | `Inter` | `22px` | 600 |
| Headings h3 | `Inter` | `18px` | 600 |
| Labels | `Inter` | `13px` | 500 |
| Mono/Code | `JetBrains Mono` | `13px` | 400 |

### 1.3 Spacing & Radius

| Token | Value |
|---|---|
| `--space-xs` | `4px` |
| `--space-sm` | `8px` |
| `--space-md` | `16px` |
| `--space-lg` | `24px` |
| `--space-xl` | `32px` |
| `--space-2xl` | `48px` |
| `--radius-sm` | `6px` |
| `--radius-md` | `10px` |
| `--radius-lg` | `16px` |
| `--radius-full` | `9999px` |

### 1.4 Shadows & Effects

| Token | Value |
|---|---|
| `--shadow-card` | `0 1px 4px rgba(0,0,0,0.06), 0 2px 8px rgba(70,166,255,0.04)` |
| `--shadow-modal` | `0 4px 24px rgba(0,0,0,0.12)` |
| `--glass-bg` | `rgba(255, 255, 255, 0.85)` with `backdrop-filter: blur(12px)` |

---

## 2. Layout Structure

### 2.1 App Shell

```
┌──────────────────────────────────────────────────────────┐
│  Top Navbar (64px)                         [🔔] [Avatar] │
├────────────┬─────────────────────────────────────────────┤
│            │                                             │
│  Sidebar   │         Main Content Area                   │
│  (240px)   │         (flex-1, scrollable)                │
│            │                                             │
│  - Groups  │                                             │
│  - Members │                                             │
│  - Temps   │                                             │
│  - Mails   │                                             │
│  - Notifs  │                                             │
│  - Settings│                                             │
│            │                                             │
├────────────┴─────────────────────────────────────────────┤
```

- **Navbar:** fixed top, glass background, logo left, notification bell + user avatar right
- **Sidebar:** fixed left, collapsible on mobile (hamburger), shows group-context navigation
- **Main content:** scrollable, max-width `1200px` centered with `--space-xl` padding

### 2.2 Responsive Breakpoints

| Name | Width | Sidebar |
|---|---|---|
| Desktop | `≥ 1024px` | Expanded (240px) |
| Tablet | `768–1023px` | Collapsed (icons only, 64px) |
| Mobile | `< 768px` | Hidden, hamburger toggle |

---

## 3. Pages

### 3.1 Landing Page (`/`)

**Purpose:** Marketing/intro page for unauthenticated users.

**Sections:**
1. **Hero** — tagline, brief description, CTA buttons ("Get Started", "Sign In")
2. **Features** — 3-column grid with icons: AI drafting, approval workflow, team collaboration
3. **Footer** — minimal links

**Design notes:**
- Full-width, no sidebar
- Gradient accent background on hero
- Subtle scroll animations (fade-in on scroll)

---

### 3.2 Auth Page (`/auth`)

**Purpose:** Login and register on a single page with a tab toggle.

**Layout:**
```
┌──────────────────────────────────────┐
│          Logo + App Name             │
│                                      │
│    ┌─────────┬──────────┐            │
│    │  Login  │ Register │  (tabs)    │
│    └─────────┴──────────┘            │
│                                      │
│    ┌──────────────────────┐          │
│    │  Email               │          │
│    │  Password            │          │
│    │  [Name - register]   │          │
│    │                      │          │
│    │  [Submit Button]     │          │
│    │                      │          │
│    │  ── or ──            │          │
│    │                      │          │
│    │  [Sign in w/ Google] │          │
│    └──────────────────────┘          │
│                                      │
└──────────────────────────────────────┘
```

- Centered card on `--bg-primary` background
- Google button with official branding
- Tab switch animates form fields (name field slides in/out)
- Email verification banner shown after registration

---

### 3.3 Dashboard (`/dashboard`)

**Purpose:** Overview of user's groups and quick actions.

**Layout:**
- **Header:** "Your Groups" title + "Create Group" button (admin+ only)
- **Grid:** Cards for each group showing name, description, member/template count, user's role badge
- **Empty state:** Illustration + "You haven't been added to any groups yet"

**Group card design:**
```
┌─────────────────────────────┐
│  Marketing Team        👥 12│
│  Email templates for...     │
│                             │
│  📋 5 templates  ✉️ 23 mails│
│  Role: moderator            │
└─────────────────────────────┘
```

- Cards have hover lift effect (`transform: translateY(-2px)`)
- Role shown as colored badge (`--accent` for moderator, `--success` for admin+)
- Admin users see a toggle: "My Groups" / "All Groups"

---

### 3.4 Group Page (`/groups/[groupId]`)

**Purpose:** Main workspace for a specific group.

**Layout:** App shell with sidebar navigation contextual to the group.

**Sidebar items:**

| Item | Icon | Visible to |
|---|---|---|
| Members | `👥` | All members |
| Templates | `📋` | All members |
| Mails | `✉️` | All members |
| Notifications | `🔔` | All members |
| Settings | `⚙️` | `admin+` only |

Each sidebar item loads a different sub-view in the main content area.

---

#### 3.4.1 Members Sub-page

- Table/list of group members with avatar, name, email, role badge
- Search/filter bar
- "Add Member" button (admin+ only) → opens modal with user search
- Role dropdown per member (admin+ only, restricted by assignment rules)
- Remove member action (admin+ only) with confirmation dialog

---

#### 3.4.2 Templates Sub-page

- Grid of template cards: name, description, field count, creator name
- "Create Template" button (moderator+ only) → navigates to template creation page
- "Add Existing Template" button (moderator+ only) → modal with template search
  - Toggle: "My Templates" / "All Templates" (admin+ sees all)
- Click template card → template detail view (prompt preview, fields list)

---

#### 3.4.3 Mails Sub-page

- Table of mails with columns: subject, creator, status badge, created date, actions
- Status badges use semantic colors:
  - `draft` → `--text-muted`
  - `pending_approval` → `--warning`
  - `approved` → `--success`
  - `rejected` → `--danger`
  - `sent` → `--info`
- Filter tabs: All | Draft | Pending | Approved | Sent | Rejected
- "Compose Mail" button → navigates to mail creation page
- Click row → opens mail detail / review page

---

#### 3.4.4 Notifications Sub-page

- Chronological list of notifications for this group
- Unread items have left accent border
- Click notification → navigates to related mail or member
- "Mark All Read" button

---

#### 3.4.5 Settings Sub-page (admin+ only)

- **Group info:** edit name, description
- **SMTP config:** email input, encrypted password input, test connection button
- **Danger zone:** delete group (owner+ only) with confirmation

---

### 3.5 Mail Creation Page (`/groups/[groupId]/mails/new`)

**Purpose:** Central, dynamic page for composing AI-assisted emails.

**This is the most important page in the application.**

#### Phase 1: Template Selection & Field Entry (centered)

```
┌──────────────────────────────────────────────┐
│                                              │
│         Select Template  [dropdown]          │
│                                              │
│         ┌──────────────────────┐             │
│         │  Meeting Topic       │             │
│         │  [text input]        │             │
│         │                      │             │
│         │  Attendees           │             │
│         │  [textarea]          │             │
│         │                      │             │
│         │  Tone                │             │
│         │  [formal ▾]          │             │
│         │                      │             │
│         │  Additional Info     │             │
│         │  [textarea]          │             │
│         │                      │             │
│         │  Subject             │             │
│         │  [text input]        │             │
│         │                      │             │
│         │  Recipients          │             │
│         │  [user search chips] │             │
│         │                      │             │
│         │  [Generate Draft ▶]  │             │
│         └──────────────────────┘             │
│                                              │
└──────────────────────────────────────────────┘
```

- Form is centered (max-width `600px`)
- Template dropdown dynamically renders fields based on selection
- Recipients use a chip-input with user search (typeahead, searches group members)
- "Additional Info" textarea at the end for extra context

#### Phase 2: Split Pane — Fields + Editor (after "Generate Draft")

**Transition animation:** form slides left, editor panel fades in from right.

```
┌──────────────────┬───────────────────────────┐
│  Fields (40%)    │  Email Editor (60%)        │
│                  │                            │
│  [Template]      │  Subject: ...              │
│  [Field 1]       │  ─────────────────         │
│  [Field 2]       │                            │
│  [...]           │  Dear team,                │
│  [Additional]    │                            │
│  [Recipients]    │  Following our meeting     │
│                  │  on Q1 Planning...         │
│                  │                            │
│  [Regenerate]    │  ~~original text~~         │
│                  │  ++edited text++           │
│                  │                            │
│                  │                            │
│──────────────────│────────────────────────────│
│                  │  [Save Draft] [Submit ▶]   │
└──────────────────┴───────────────────────────┘
```

- **Left pane:** same form fields, now editable for regeneration
- **Right pane:** rich text editor (e.g. Tiptap or Lexical)
- **Diff display:** user edits shown as inline diffs (green for additions, red for deletions) toggled via a "Show Changes" button
- **Actions:**
  - "Regenerate" — re-calls LLM with updated fields, resets editor
  - "Save Draft" — saves current state
  - "Submit for Approval" — changes status to `pending_approval`

---

### 3.6 Mail Review Page (`/groups/[groupId]/mails/[mailId]`)

**Purpose:** Moderators/admins review submitted mails.

**Layout:** Similar to Phase 2 of mail creation, but read-only fields on left.

- **Left pane:** read-only field values, template info, creator info, status timeline
- **Right pane:** editor with diff view (original vs final), editable by reviewer
- **Actions (moderator+ only):**
  - "Approve" → status to `approved`, optionally edit before approving
  - "Reject" → opens reason input, status to `rejected`
  - "Approve & Send" → approve and immediately send via SMTP

**Status timeline:**
```
● Created (Jan 15, 10:00 AM) — by Jane
● Submitted (Jan 15, 10:30 AM) — by Jane
● Approved (Jan 15, 11:00 AM) — by Admin Bob
● Sent (Jan 15, 11:01 AM)
```

---

### 3.7 Template Creation Page (`/templates/new`)

**Purpose:** AI-assisted template builder for moderators.

#### Step 1: Describe the template

```
┌──────────────────────────────────────┐
│  What kind of email template?        │
│  [textarea: describe your template]  │
│                                      │
│  [Generate Template ▶]              │
└──────────────────────────────────────┘
```

#### Step 2: Answer refinement questions (MCQs from LLM)

```
┌──────────────────────────────────────┐
│  Formality level?                    │
│  ○ Very formal  ● Formal  ○ Casual  │
│                                      │
│  Include action items section?       │
│  ● Yes  ○ No                         │
│                                      │
│  Typical length?                     │
│  ○ Short  ● Medium  ○ Long          │
│                                      │
│  [Finalize Template ▶]              │
└──────────────────────────────────────┘
```

#### Step 3: Review & save

- Preview shows the generated prompt and fields
- User can edit prompt text, add/remove/reorder fields
- "Save Template" button

---

## 4. Shared Components

| Component | Description |
|---|---|
| `Navbar` | Glass-effect top bar, logo, notification bell with unread count, user avatar dropdown |
| `Sidebar` | Collapsible, icon + label items, active state highlight, group-context aware |
| `Badge` | Role/status badges with semantic colors and pill shape |
| `Button` | Primary (accent), secondary (outlined), danger (red), ghost (text-only), all with hover/active states |
| `Card` | `--bg-secondary` background, `--radius-md` corners, `--shadow-card`, hover lift |
| `Modal` | Centered overlay with `--shadow-modal`, backdrop blur, slide-up animation |
| `Table` | Striped rows, hover highlight, sortable column headers |
| `ChipInput` | For recipients — typeahead search, removable chips |
| `DiffViewer` | Inline diff display with green/red highlighting, toggle on/off |
| `RichTextEditor` | Tiptap or Lexical-based, toolbar with basic formatting |
| `StatusTimeline` | Vertical timeline with colored dots per status change |
| `Toast` | Bottom-right notification toasts for success/error/info |
| `Skeleton` | Loading state placeholders matching component shapes |
| `EmptyState` | Illustration + message + CTA button |

---

## 5. Animations & Micro-interactions

| Interaction | Animation |
|---|---|
| Page transitions | Fade + slight slide (150ms ease) |
| Mail page split reveal | Left pane slides from center to left (300ms ease-out), right pane fades in (200ms delay) |
| Card hover | `translateY(-2px)` + shadow increase (150ms) |
| Sidebar collapse | Width transition (200ms ease) |
| Modal open | Backdrop fade (150ms) + modal slide-up (200ms) |
| Badge appear | Scale from 0.8 → 1.0 (100ms) |
| Toast enter/exit | Slide in from right (200ms), auto-dismiss after 4s |
| Button click | Scale 0.97 → 1.0 (100ms) |
| Form field focus | Border color transition (150ms) + subtle glow |
| Diff highlights | Fade in with 100ms delay per line |

---

## 6. Route Map

| Route | Page | Auth Required | Min Role |
|---|---|---|---|
| `/` | Landing | No | — |
| `/auth` | Login / Register | No | — |
| `/dashboard` | Dashboard | Yes | `user` |
| `/groups/[groupId]` | Group (redirects to mails) | Yes | member |
| `/groups/[groupId]/members` | Group Members | Yes | member |
| `/groups/[groupId]/templates` | Group Templates | Yes | member |
| `/groups/[groupId]/mails` | Group Mails | Yes | member |
| `/groups/[groupId]/mails/new` | Mail Creation | Yes | member |
| `/groups/[groupId]/mails/[mailId]` | Mail Detail / Review | Yes | member |
| `/groups/[groupId]/notifications` | Group Notifications | Yes | member |
| `/groups/[groupId]/settings` | Group Settings | Yes | `admin+` |
| `/templates/new` | Template Creation | Yes | `moderator+` |
