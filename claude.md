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
- **Location**: `/app/`
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

## Authentication Flow

### Current Implementation
1. **Login/Register** → API call with credentials
2. **Token Response** → Backend returns `access_token`, `token_type`, `expires_in`, `user_id`
3. **User Data Fetch** → Frontend calls `/api/v1/me` to get complete user object
4. **State Update** → Store user data + token in userStore
5. **Navigation** → Redirect to dashboard

### Key Files
- **Backend**: `app/api/routes/auth.py`, `app/core/exceptions.py`
- **Frontend**: `services/authService.ts`, `stores/userStore.ts`, `api/auth.ts`

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

## Authentication State Management

### UserStore Structure
```typescript
{
  user: User | null,           // Complete user object
  isLoading: boolean,          // Loading states
  isAuthenticated: computed,   // Derived from user presence
  preferences: object          // User preferences
}
```

### Auth Service Methods
- `login(credentials)` - Handle login + user fetch + navigation
- `register(userData)` - Handle registration + user fetch + navigation  
- `logout()` - Clear state + navigate home
- `checkAuthStatus()` - Verify token validity on app start

## Component Development Guidelines

### Form Components
- **Validation**: Inline validation in event handlers
- **Error Handling**: Local error state with user-friendly messages
- **Loading States**: Use store loading state
- **Events**: Emit meaningful events for parent components

### Dashboard Components (Planned)
- **Modular Structure**: Break dashboard into logical components
- **Separation of Concerns**: UI components, data components, action components
- **Reusability**: Build components that can be reused across different dashboard views

## Development Workflow

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

## Dashboard Architecture Implementation

The dashboard has been implemented using a **component-based architecture** with clear separation of concerns:

### Main Dashboard Components

1. **DashboardHome.vue** - Main container component
   - Orchestrates the overall dashboard layout
   - Manages state flow between child components
   - Handles navigation and user interactions
   - Includes header with user profile and stats

2. **JobInputCard.vue** - Job description input and analysis
   - Company name and job title input fields
   - Job description textarea with character count
   - Real-time keyword extraction and requirements detection
   - Debounced analysis to avoid excessive API calls
   - Preview of detected requirements as tags
   - Submit button with processing state

3. **ProfileSetupCard.vue** - User profile management
   - Progress tracking with completion percentage
   - Basic info (name, email, phone, location)
   - Skills management with add/remove functionality
   - Professional summary editing
   - Expandable form interface with sections
   - LinkedIn import placeholder

4. **ResumePreviewCard.vue** - Generated resumes display
   - Grid and list view toggle modes
   - Resume thumbnails with mock previews
   - Match percentage indicators
   - Download and delete action buttons
   - Empty state for first-time users
   - Pagination support for large resume collections

### Workflow Integration

The dashboard implements the core user workflow:
```
Step 1: Profile Setup → Step 2: Job Input → AI Processing → Resume Generation → Preview & Download
```

### Component Communication Patterns

- **Event-driven communication**: Child components emit events to parent
- **Props for configuration**: Parent passes configuration to children
- **Store integration**: Components access user state through userStore
- **Local state management**: Each component manages its own UI state

### Development Patterns Used

- **TypeScript interfaces** for type safety
- **Composable patterns** for reusable logic
- **Mock data** for development and testing
- **TODO markers** for future API integration points
- **Responsive design** with Tailwind CSS utilities

## Recent Updates & Current State (August 2025)

### Dashboard Implementation
- **Main Component**: `DashboardHome.vue` - Complete dashboard with 3-step workflow
- **Step 1**: Profile enhancement with 3 horizontal action buttons
  - Add Profile Sections
  - Extract from Resume 
  - Import LinkedIn Profile
- **Step 2**: Job input via `JobInputCard.vue`
- **Step 3**: Resume generation results with preview and download options

### UI/UX Improvements
- **Enhanced Light Mode**: Improved contrast with better background colors
  - Changed main background from pure white to `gray-100`
  - Enhanced card shadows and borders for better visual hierarchy
  - Strengthened gradient backgrounds and button styling
- **Simplified Navigation**: Minimal auth layout with just dark mode toggle and logout
- **Horizontal Button Layout**: Three main action buttons now display horizontally for space efficiency

### Component Cleanup
- **Removed Unnecessary Files**: Cleaned up dashboard folder
- **Kept Essential Components**: 
  - `DashboardHome.vue` (main dashboard)
  - `JobInputCard.vue` (job input functionality)
  - `ResumePreviewCard.vue` (resume preview/management)
- **Removed Files**: DashboardHeader.vue, DashboardNavigation.vue, Header.vue, Navigation.vue, QuickActionCard.vue, RecentActivity.vue

### Authentication Layout
- **Simplified Design**: `layouts/auth.vue` with minimal top bar
- **Features**: Logo, dark mode toggle, logout button only
- **Background**: Enhanced with `gray-100` background and shadow for better contrast

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

/app/                         # FastAPI Backend
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

## File Structure
```
/app/                          # FastAPI Backend
├── api/routes/               # API routes
├── core/                     # Core configuration
├── db/                       # Database layer
└── features/                 # Business logic

/frontend/app/                # Nuxt 3 Frontend  
├── components/              # Vue components
│   ├── auth/               # Authentication components
│   └── dashboard/          # Dashboard components (planned)
├── services/               # Business logic services
├── stores/                 # State management
├── api/                    # HTTP client functions
├── middleware/             # Route middleware
├── pages/                  # Page components
└── plugins/                # Nuxt plugins
```

## Notes for Claude
- **Prefer simplicity** over complex abstractions
- **Ask clarifying questions** about architecture decisions
- **Reference this file** for context and patterns
- **Suggest improvements** aligned with established patterns
- **Focus on maintainability** and code clarity

---

*Last Updated: August 18, 2025*
*Current Focus: Dashboard component architecture planning*
