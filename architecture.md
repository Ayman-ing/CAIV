# CAIV — Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Frontend (Nuxt 3 SPA)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │  Pages   │  │Components│  │ Stores   │  │     Services       │  │
│  │ (9 pages)│  │(30+ comp)│  │(reactive)│  │ (auth, profile,    │  │
│  │          │  │          │  │          │  │  resume, sections) │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬───────────┘  │
│       └──────────────┴─────────────┴─────────────────┘              │
│                              │ $fetch + JWT                         │
└──────────────────────────────┼──────────────────────────────────────┘
                               │ HTTP :8000
┌──────────────────────────────┼──────────────────────────────────────┐
│                    Backend (FastAPI)                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │  Routes  │→ │ Service  │→ │Repository│→ │   SQLAlchemy DB    │  │
│  │(feature- │  │ (business│  │ (data    │  │  (PostgreSQL +     │  │
│  │ based)   │  │  logic)  │  │  access) │  │   pgvector)        │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────────┘  │
│                                                    ↑                │
│  ┌──────────────────────────────────────────────────┘               │
│  │                                                                  │
│  ├── LLM Service (Groq) ←── PDF Parser (Docling) ←── Resume Upload │
│  ├── Vector Embeddings (sentence-transformers → pgvector)          │
│  └── Celery (Redis broker → async background tasks)                │
└─────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Nuxt 4 (Vue 3), SSR disabled | SPA client |
| **Styling** | Tailwind CSS, custom UI components | Design system |
| **Backend** | FastAPI (Python 3.12) | REST API |
| **Database** | PostgreSQL 16 + pgvector | Relational + vector storage |
| **ORM** | SQLAlchemy 2.0 + Alembic | Migrations & queries |
| **Auth** | JWT (python-jose, passlib/bcrypt) | Authentication |
| **AI/LLM** | Groq (llama-3.3-70b-versatile) | Resume parsing |
| **PDF** | Docling (CPU mode) | PDF text extraction |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2, 384d) | Vector generation |
| **Queue** | Celery + Redis | Async background tasks |
| **Container** | Docker (pgvector, Redis) | Infrastructure |

## Directory Layout

```
/
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI entry point (uvicorn)
│       ├── core/                   # Config, exceptions, logging, celery
│       ├── db/                     # SQLAlchemy engine & sessions
│       ├── shared/models/          # Base entity classes
│       ├── features/               # Feature modules (see below)
│       ├── tests/                  # Pytest test suite
│       └── alembic/                # Database migrations
├── frontend/
│   └── app/
│       ├── app.vue                 # Root component
│       ├── pages/                  # 9 page routes
│       ├── components/             # UI + feature components
│       ├── api/                    # HTTP client ($fetch) per domain
│       ├── services/               # Business logic orchestration
│       ├── stores/                 # Reactive state (user, profile)
│       ├── composables/            # Reusable Vue composables
│       ├── middleware/             # Auth/guest route guards
│       ├── plugins/                # Client-side init plugins
│       └── layouts/                # auth.vue layout
├── docker-compose.yml              # PostgreSQL + Redis
└── docs/                           # Project documentation
```

## Backend Architecture

### Feature Module Pattern

Every feature follows: **Router → Service → Repository → DB**

```
features/<feature_name>/
├── __init__.py        # Re-exports
├── models.py          # SQLAlchemy model
├── schemas.py         # Pydantic (Create/Update/Response)
├── service.py         # Business logic
├── repository.py      # DB operations
└── router.py          # API endpoints
```

Auth guard injected at router level via `Depends(get_current_user)`.

### Features List

| Feature | Routes | Description |
|---------|--------|-------------|
| `auth` | `/api/v1/auth/*` | Register, login, logout, password reset |
| `users` | `/api/v1/me`, `/api/v1/{uuid}` | User CRUD, admin promotion |
| `profiles` | `/api/v1/profiles/*` | Profile CRUD, embedding indexing |
| `profiles/work_experiences` | `/profiles/{uuid}/work-experiences/*` | Work history |
| `profiles/education` | `/profiles/{uuid}/education/*` | Education history |
| `profiles/skills` | `/profiles/{uuid}/skills/*` | Skills |
| `profiles/projects` | `/profiles/{uuid}/projects/*` | Projects |
| `profiles/certificates` | `/profiles/{uuid}/certificates/*` | Certifications |
| `profiles/languages` | `/profiles/{uuid}/languages/*` | Languages |
| `profiles/custom_sections` | `/profiles/{uuid}/custom-sections/*` | Custom sections |
| `profiles/profile_links` | `/profiles/{uuid}/links/*` | Social/portfolio links |
| `profiles/professional_summaries` | `/profiles/{uuid}/professional-summaries/*` | Summaries |
| `job_descriptions` | `/api/v1/users/{uuid}/job-descriptions/*` | Job postings |
| `resumes` | `/api/v1/profiles/{uuid}/resumes/*` | Generated resumes + components |
| `resume_import` | `/api/v1/resume-import/*` | PDF upload + AI parsing |
| `vector_embeddings` | (internal) | Embedding generation, Celery tasks |
| `llm` | (internal) | Groq LLM provider + strategy pattern |
| `tasks` | `/api/v1/tasks/{task_id}` | Celery task status polling |

### Database Schema

#### Polymorphic Entity Inheritance

```
entities (parent table)
  ├── work_experiences
  ├── education
  ├── skills
  ├── projects
  ├── certificates
  ├── languages
  ├── custom_sections
  ├── profile_links
  ├── professional_summaries
  ├── job_descriptions
  └── generated_resumes
```

All entities share `entities.id` as primary key via FK. The `Entity.uuid` column acts as the target for vector embeddings (1:N with `embeddings` table).

#### Core Tables

- **users** — Auth, roles (user/admin), timestamps
- **profiles** — 1:1 with users, holds contact info
- **entities** — Polymorphic parent, uuid + entity_type discriminator
- **work_experiences, education, skills, etc.** — Profile sub-entities inheriting from Entity
- **job_descriptions** — User-submitted job postings
- **job_keywords, job_requirements** — Parsed from job descriptions
- **generated_resumes** — Output resumes, linked to profile + job description
- **resume_components** — Line items within a generated resume
- **uploaded_resumes** — Imported PDFs with extraction status
- **embeddings** — pgvector(384) vectors, linked to entities.uuid
- **outbox_events** — Event log for async processing

### Key Relationships

- **User 1:1 Profile** — Auto-created on registration
- **Profile 1:N Entities** — Work experience, education, skills, etc.
- **Entity 1:N Embeddings** — Via Entity.uuid FK
- **Profile 1:N GeneratedResumes** — Multiple saved resume versions
- **JobDescription 1:N GeneratedResumes** — Resumes can target a specific job

### Infrastructure

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL + pgvector | 5432 | Primary DB + vector storage |
| Redis | 6379 | Celery broker + backend |
| FastAPI | 8000 | REST API |
| Nuxt (dev) | 3000 | Frontend dev server |

## Frontend Architecture

### Data Flow

```
Pages → Components ←→ Services → API Layer ($fetch) → Backend
                         ↕
                    Stores (reactive)
```

### Pages & Routing

| Route | Page | Auth | Layout |
|-------|------|------|--------|
| `/` | Landing (Hero, Features) | Guest | Default |
| `/login` | Login form | Guest | Default |
| `/register` | Registration form | Guest | Default |
| `/dashboard` | 3-step workflow hub | Required | auth |
| `/profile` | Profile sections editor | Required | auth |
| `/cv-editor` | 3-panel resume builder | Required | auth |
| `/extract-resume` | PDF upload + AI import | Required | auth |
| `/components` | UI component showcase | None | Default |

### Component Architecture

- **`components/ui/`** — Design system: Button, Input, Card, Modal, Toast, CollapsibleSection, DarkModeToggle
- **`components/profile/`** — 10 section editors (basicInfo, experience, education, skills, projects, certification, language, links, professionalSummary, custom)
- **`components/cv-editor/`** — 3-panel layout (LeftSidebar, CenterCanvas, RightSidebar)
- **`components/dashboard/`** — DashboardHome, JobInputCard, ResumePreviewCard
- **`components/auth/`** — LoginForm, RegisterForm
- **`components/sections/`** — Landing page (Navigation, Hero, Features, Footer)

Each profile section follows the pattern: `CollapsibleSection` wrapper → `Modal` for add/edit → inline delete confirmation.

### State Management

| Store | State | Description |
|-------|-------|-------------|
| `userStore` | user, isLoading, preferences | Auth state + user data |
| `profileStore` | profiles[], activeProfile | Profile CRUD state |

Both use simple reactive singletons (no Pinia).

### Composables

| Composable | Purpose |
|------------|---------|
| `useDarkMode` | Theme toggle with localStorage + system preference |
| `useToast` | Global toast notification system |
| `useFormValidation` | Reusable field validation (length, range, dates, required) |
| `useUrlValidator` | URL validation matching Pydantic's HttpUrl |
| `useProfileIndexing` | Profile embedding indexing with Celery task polling |
| `useCVEditor` | Full CV editor state machine (resume CRUD, components, templates, preview) |

### Auth Flow

```
Login → JWT token → localStorage → auth.client.ts plugin restores on refresh
                                        → middleware/auth.ts guards protected routes
                                        → middleware/guest.ts redirects authenticated users from login/register
```

## AI/ML Pipeline

### Resume Import Pipeline

```
PDF Upload (multipart)
    │
    ▼
Docling (CPU) → Markdown text extraction
    │
    ▼
Groq LLM (function calling, llama-3.3-70b) → Structured ResumeData
    │
    ▼
UploadedResume (status: pending) → User confirms via /confirm
    │
    ▼
_populate_profile() → maps data to 8 profile sub-features
    │                   └── Failed items → CustomSection (graceful degradation)
    ▼
Services: EducationService, WorkExperienceService, SkillService, etc.
```

### Embedding Indexing Pipeline

```
Index profile request (/profiles/{uuid}/index)
    │
    ▼
Celery task: index_profile_task
    │
    ▼
For each entity in profile → TextFormatter → sentence-transformers → pgvector(384)
    │
    ▼
Tasks status polled via /api/v1/tasks/{task_id}
```

### LLM Architecture

Strategy pattern with `LLMProvider` protocol:

```
LLMService.parse_to_model_with_function_calling()
    │
    ├── GroqProvider.parse_with_function_calling()
    │       ├── Pydantic → Groq function definition (with $ref inlining, anyOf handling)
    │       ├── API call → JSON response
    │       └── 3-tier fallback: direct parse → escape cleanup → regex extraction
    │
    └── Returns Pydantic model with 100% schema compliance
```

## Coding Conventions

- **Backend**: Sync DB for request-response, async DB for Celery tasks
- **Backend**: UUID-based resource addressing, internal integer IDs for FKs
- **Frontend**: `<script setup lang="ts">` SFCs, simple functions over classes
- **Frontend**: Custom stores over Pinia, inline validation over composable factories
- **Error handling**: Custom `HTTPException` with `message` field (mapped to FastAPI `detail`)
- **PDF parsing**: Failsafe — validation failures degrade to CustomSection, never lose data
