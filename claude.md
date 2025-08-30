# AI Resume Builder (CAIV) - Project Documentation

## Project Overview
CAIV is a full-stack AI-powered resume builder application with FastAPI backend and Nuxt.js frontend.

**Core Workflow**: The app focuses on creating tailored resumes based on pasted job descriptions. Users upload/create their profile data, paste job descriptions, and the system uses hybrid search (semantic + keyword) to intelligently select the best profile elements that match the job requirements.

### Key User Journey
1. **Setup Profile** - Create profile manually, upload existing resume, or import LinkedIn
2. **Input Job Description** - Paste target job posting  
3. **AI Processing** - Hybrid search matches profile elements to job requirements
4. **Resume Generation** - Create tailored resume optimized for the specific job
5. **Review & Export** - Edit, preview, and download the generated resume

## Architecture

### Documentation
- **Location**: `/docs/` - Comprehensive project documentation
- **Files**:
  - `development-guide.md` - Development setup and workflows
  - `api-documentation.md` - API endpoints and schemas
  - `database-schema.md` - Database structure and relationships
  - `REFACTORING_COMPLETE.md` - Latest refactoring documentation
  - Various specialized docs for entity systems, vector embeddings, etc.

### Backend (FastAPI)
- **Location**: `backend/app/`
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT Bearer tokens
- **API Structure**: RESTful API with `/api/v1/` prefix
- **Error Handling**: Custom HTTPException using `message` field (mapped to FastAPI's `detail`)

### Frontend (Nuxt.js)
- **Location**: `/frontend/app/`
- **Framework**: Nuxt 3 with TypeScript
- **Styling**: Tailwind CSS with enhanced light mode contrast
- **State Management**: Custom reactive stores (no Pinia)
- **Authentication**: JWT tokens stored in localStorage
- **Layout System**: `auth.vue` layout for protected routes with minimal navigation




## Project Patterns & Conventions

### Code Simplification Philosophy
- ✅ **Direct inline logic** over unnecessary abstraction layers
- ✅ **Simple functions** over complex class hierarchies  
- ✅ **Minimal composables** - only for truly reusable utilities
- ✅ **Component-level validation** - put logic where it's used
- ✅ **Single responsibility** - services for business logic, stores for state
- ✅ **SFC** - always start with the \<script setup lang='fr'> than the template

### Avoided Anti-Patterns
- ❌ Over-engineered composables with pass-through methods
- ❌ Complex singleton classes for simple operations
- ❌ Unnecessary abstraction layers
- ❌ Polling-based initialization systems

### Frontend Architecture

#### Services Layer (`/services/`)
- **Purpose**: Business logic and API coordination
- **Pattern**: Simple object exports with methods
- **Example**: `authService.ts` - handles login/register flow + navigation

#### Stores (`/stores/`)
- **Purpose**: Reactive state management
- **Pattern**: Composable functions returning reactive state + actions
- **Example**: `userStore.ts` - user authentication state

#### Components (`/components/`)
- **Structure**: 
  - `auth/` - Authentication forms (LoginForm, RegisterForm)
  - `dashboard/` - Dashboard-specific components (planned)
- **Pattern**: Self-contained validation and logic, emit events for parent communication

#### Middleware (`/middleware/`)
- **auth.ts**: Protects authenticated routes
- **guest.ts**: Redirects authenticated users from login/register
- **Pattern**: Simple, direct checks using userStore

#### API Layer (`/api/`)
- **Purpose**: HTTP client functions for backend communication
- **Pattern**: Simple async functions with error handling
- **Error Handling**: Maps backend errors to frontend-friendly format

## Component Development Guidelines

### Form Components
- **Validation**: Inline validation in event handlers
- **Error Handling**: Local error state with user-friendly messages
- **Loading States**: Use store loading state

### Current Status
- ✅ Authentication system complete and working
- ✅ User state management implemented
- ✅ Login/Register components refactored and simplified
- ✅ Middleware and routing protection working
- ✅ **Dashboard Architecture**: Complete with modular component structure
- 🔄 **Next**: API integration and AI resume generation backend

### Immediate Next Steps
1. **Dashboard Architecture**: Plan component separation
2. **Component Creation**: Build modular dashboard components
3. **Data Management**: Implement dashboard-specific stores/services
4. **UI/UX**: Create responsive and intuitive dashboard interface



### Workflow Integration

The dashboard implements the core user workflow:
```
Step 1: Profile Setup → Step 2: Job Input → AI Processing → Resume Generation → Preview & Download
```



### Development Patterns Used

- **TypeScript interfaces** for type safety
- **Composable patterns** for reusable logic
- **Mock data** for development and testing
- **TODO markers** for future API integration points
- **Responsive design** with Tailwind CSS utilities







### Dark Mode Integration
- **Composable**: `useDarkMode()` with toggle functionality
- **Persistence**: Settings saved to localStorage
- **Theme Application**: Auto-applies theme on mount with system preference fallback

## File Structure
```
/docs/                        # Project Documentation
├── development-guide.md      # Setup and development workflows
├── api-documentation.md      # API endpoints and schemas
├── database-schema.md        # Database structure
└── [various specialized docs]

/backend/app/                         # FastAPI Backend
├── api/routes/              # API routes
├── core/                    # Core configuration
├── db/                      # Database layer
└── features/                # Business logic

/frontend/app/               # Nuxt 3 Frontend  
├── components/              # Vue components
│   ├── auth/               # Authentication components
│   └── dashboard/          # Dashboard components (cleaned up)
│       ├── DashboardHome.vue    # Main dashboard component
│       ├── JobInputCard.vue     # Job input functionality
│       └── ResumePreviewCard.vue # Resume preview/management
├── layouts/                 # Layout components
│   └── auth.vue            # Simplified authenticated layout
├── services/               # Business logic services
├── stores/                 # State management
├── api/                    # HTTP client functions
├── middleware/             # Route middleware
├── pages/                  # Page components
└── plugins/                # Nuxt plugins
```

## Technical Decisions Made

### Why Simple Functions Over Classes?
- ✅ Better compatibility with Vue 3 Composition API
- ✅ Easier testing and debugging
- ✅ No context/scope issues with composables
- ✅ More functional programming approach

### Why Custom Stores Over Pinia?
- ✅ Learning exercise and full control
- ✅ Simpler for project scope
- ✅ No additional dependencies
- ✅ Easier to understand and customize

### Why Inline Validation?
- ✅ Clearer code - see validation logic where it's used
- ✅ Less function overhead
- ✅ Easier maintenance
- ✅ No unnecessary abstraction


## Notes for Claude
- **Prefer simplicity** over complex abstractions
- **Ask clarifying questions** about architecture decisions
- **Reference this file** for context and patterns
- **Suggest improvements** aligned with established patterns
- **Focus on maintainability** and code clarity

---

*Last Updated: August 30, 2025*
