# AI Resume Builder (CAIV)

An intelligent resume building platform that leverages AI to create personalized, ATS-optimized resumes tailored to specific job descriptions.

## 🚀 Features

- **Profile-Based Architecture**: Separate user authentication from resume data
- **AI-Powered Resume Generation**: Generate resumes optimized for specific job descriptions
- **Vector Embeddings**: Advanced matching between profiles and job requirements
- **ATS Optimization**: Ensure resumes pass Applicant Tracking Systems
- **Multiple Resume Variants**: Generate different resumes for different job applications
- **Comprehensive Profile Management**: Education, experience, skills, projects, certifications, and more

## 🏗️ Architecture

### Database Schema

The application uses a PostgreSQL database with the following structure:

#### Core Tables
- **`users`** - User authentication and basic info
- **`profiles`** - User profiles (separated from auth)
- **`generated_resumes`** - Generated resume documents
- **`resume_components`** - Individual resume sections

#### Job-Related Tables
- **`job_descriptions`** - Job postings and requirements
- **`job_keywords`** - Extracted job keywords
- **`job_requirements`** - Structured job requirements

#### Profile Detail Tables
- **`education`** - Education history
- **`work_experiences`** - Work experience entries
- **`projects`** - Personal/professional projects
- **`skills`** - Technical and soft skills
- **`certificates`** - Certifications and licenses
- **`languages`** - Language proficiencies
- **`professional_summaries`** - Professional summary variants
- **`profile_links`** - Social media and professional links
- **`custom_sections`** - Custom resume sections

#### System Tables
- **`outbox_events`** - Event sourcing for system events
- **`vector_embeddings`** - AI embeddings for matching (uses global entity system)

### Inheritance-Based Global Entity System

The application implements a sophisticated inheritance-based global entity system for managing AI vector embeddings:

#### Architecture Overview

**BaseEntity Class** (`shared/models/entity.py`):
- Provides a global `entity_id` (UUID) for all embeddable entities
- Automatic timestamp management (`created_at`, `updated_at`)
- Built-in relationship to vector embeddings
- Inherited by all entities that can have AI embeddings

**Entity Types**:
- **Container Entity**: `profiles` - Does NOT inherit from BaseEntity (container for entities)
- **Embeddable Entities**: All profile components inherit from BaseEntity:
  - `work_experiences`, `projects`, `education`, `skills`
  - `certificates`, `languages`, `professional_summaries`
  - `profile_links`, `custom_sections`
  - `job_descriptions`, `generated_resumes`

#### Vector Embedding System

**Before** (Multiple FK approach):
```sql
-- Old inefficient design with 12 nullable foreign keys
CREATE TABLE vector_embeddings (
    id SERIAL PRIMARY KEY,
    work_experience_id INTEGER,  -- nullable
    project_id INTEGER,          -- nullable
    education_id INTEGER,        -- nullable
    -- ... 9 more nullable FK columns
);
```

**After** (Global entity system):
```sql
-- Clean, efficient design with single global reference
CREATE TABLE vector_embeddings (
    id SERIAL PRIMARY KEY,
    entity_id UUID NOT NULL,     -- References any BaseEntity.entity_id
    qdrant_point_id UUID,
    embedding_type VARCHAR(50),
    -- ... other fields
);
```

#### Benefits

1. **Simplified Schema**: Single `entity_id` column instead of 12 nullable foreign keys
2. **No Empty Columns**: Every embedding record has exactly one entity reference
3. **Global Entity System**: Unique identifier across all embeddable entity types
4. **Extensible**: Easy to add new embeddable entity types
5. **Type Safety**: SQLAlchemy inheritance provides compile-time type checking
6. **Performance**: Better indexing and query performance with single UUID reference

#### Implementation Details

```python
# BaseEntity provides common fields and embeddings relationship
class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, unique=True, default=uuid.uuid4)
    entity_id = Column(UUID, unique=True, nullable=False)  # Global identifier
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    @declared_attr
    def embeddings(cls):
        return relationship("VectorEmbedding", cascade="all, delete-orphan")

# Profile components inherit from BaseEntity
class WorkExperience(BaseEntity):
    __tablename__ = 'work_experiences'
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    # ... specific fields
    # embeddings relationship inherited automatically

# Vector embeddings reference any entity through global entity_id
class VectorEmbedding(Base):
    __tablename__ = 'vector_embeddings'
    entity_id = Column(UUID, nullable=False)  # References BaseEntity.entity_id
    # ... other fields
```

### Technology Stack

- **Backend**: FastAPI with Python 3.12+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Package Management**: UV
- **AI/ML**: Vector embeddings for intelligent matching
- **Architecture Pattern**: Feature-based with Repository-Service-Router pattern

## 📁 Project Structure

```
app/
├── main.py                     # FastAPI application entry point
├── alembic/                    # Database migrations
│   ├── env.py                  # Alembic configuration
│   └── versions/               # Migration files
├── api/
│   ├── dependencies.py         # API dependencies
│   └── routes/
│       └── user.py            # User routes
├── core/
│   └── config.py              # Application configuration
├── db/
│   ├── database.py            # Database connection
│   └── session.py             # Database session management
├── shared/
│   └── models/
│       └── base.py            # SQLAlchemy base model
├── features/                   # Feature-based organization
│   ├── users/                 # User management
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── router.py
│   │   └── schemas.py
│   ├── profiles/              # Profile management
│   │   ├── models.py
│   │   ├── certificates/      # Certifications
│   │   ├── custom_sections/   # Custom resume sections
│   │   ├── education/         # Education history
│   │   ├── languages/         # Language skills
│   │   ├── profile_links/     # Social/professional links
│   │   ├── professional_summaries/  # Professional summaries
│   │   ├── projects/          # Projects
│   │   ├── skills/            # Skills
│   │   └── work_experiences/  # Work experience
│   ├── resumes/               # Resume generation
│   ├── job_descriptions/      # Job posting management
│   ├── job_keywords/          # Job keyword extraction
│   ├── job_requirements/      # Job requirement analysis
│   ├── outbox_events/         # Event sourcing
│   └── vector_embeddings/     # AI embeddings
├── schemas/                   # Pydantic schemas
├── services/                  # Business logic services
└── workers/                   # Background task workers
```

## 🔧 Setup and Installation

### Prerequisites

- Python 3.12+
- PostgreSQL database
- UV package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIResumeBuilder/CAIV
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and other configuration
   ```

4. **Run database migrations**
   ```bash
   cd app
   uv run alembic upgrade head
   ```

5. **Start the development server**
   ```bash
   uv run uvicorn main:app --reload
   ```

## 🗄️ Database Management

### Migrations

The project uses Alembic for database migrations:

```bash
# Generate a new migration
uv run alembic revision --autogenerate -m "Description of changes"

# Apply migrations
uv run alembic upgrade head

# Check current migration status
uv run alembic current

# View migration history
uv run alembic history
```

### Database Schema Features

- **Profile-Based Design**: Users can have multiple profiles for different career paths
- **Inheritance-Based Entity System**: Global entity identification for AI embeddings
- **Foreign Key Relationships**: Proper relational structure with referential integrity
- **UUID Support**: Public UUIDs for external API access, internal IDs for performance
- **Timestamps**: Created/updated timestamps on all entities
- **Event Sourcing**: Outbox pattern for reliable event processing

### Recent Schema Evolution

#### Migration to Inheritance-Based Global Entity System

**Migration History**:
- `4d381a20854c` - Added foreign key relationships to vector_embeddings (initial approach)
- `013fc9c3a89b` - Implemented inheritance-based global entity system
- `5adc69a5fade` - Fixed custom_sections table to match entity inheritance pattern

**Key Changes**:

1. **Vector Embeddings Simplification**:
   - **Before**: 12 nullable foreign key columns (`work_experience_id`, `project_id`, etc.)
   - **After**: Single `entity_id` (UUID) column referencing any BaseEntity

2. **Global Entity System**:
   - Added `entity_id` (UUID) column to all embeddable entities
   - Unique global identifier across all entity types
   - Automatic relationship to vector embeddings

3. **Inheritance Pattern**:
   - `BaseEntity` abstract class provides common fields and embeddings relationship
   - All profile components inherit from BaseEntity
   - Profile model remains a container (does not inherit from BaseEntity)

4. **Schema Consistency**:
   - Fixed `custom_sections` table to use `profile_id` instead of `user_id`
   - Added missing `entity_id` column to `custom_sections`
   - Consistent foreign key patterns across all profile entities

**Benefits Achieved**:
- ✅ Eliminated 12 nullable columns in vector_embeddings table
- ✅ No more empty/orphaned embedding records
- ✅ Simplified relationship management
- ✅ Better query performance with single UUID index
- ✅ Type-safe inheritance pattern
- ✅ Easy extensibility for new entity types

## 🧩 API Architecture

### Feature-Based Organization

Each feature follows a consistent pattern:

- **Models** (`models.py`): SQLAlchemy database models
- **Schemas** (`schemas.py`): Pydantic request/response models
- **Repository** (`repository.py`): Data access layer
- **Service** (`service.py`): Business logic layer
- **Router** (`router.py`): FastAPI route definitions

### API Patterns

- **UUID-based public APIs**: All external IDs use UUIDs for security
- **Consistent response format**: Standardized API responses
- **Dependency injection**: Clean separation of concerns
- **Repository pattern**: Abstracted data access

## 🤖 AI Features

### Vector Embeddings

The application uses vector embeddings for:

- **Profile-Job Matching**: Compare user profiles with job requirements
- **Content Optimization**: Suggest resume improvements
- **Keyword Extraction**: Identify important keywords from job descriptions
- **ATS Optimization**: Ensure resume content matches ATS requirements

### Resume Generation

- **Dynamic Content**: Generate resume sections based on job requirements
- **Multiple Variants**: Create different resumes for different applications
- **ATS Compliance**: Ensure generated content is ATS-friendly
- **Personalization**: Tailor content to specific job descriptions

## 📊 Current Status

### ✅ Completed

- [x] Complete database schema design (18 tables)
- [x] All SQLAlchemy models implemented
- [x] Database migrations configured and applied
- [x] Feature-based project structure
- [x] Profile-based architecture implemented
- [x] Repository-Service-Router pattern established

### 🚧 In Progress

- [ ] API route implementations
- [ ] Authentication and authorization
- [ ] Resume generation logic
- [ ] AI integration for content optimization
- [ ] Vector embedding implementation

### 📋 Upcoming

- [ ] Frontend application
- [ ] PDF generation
- [ ] Email notifications
- [ ] Job board integrations
- [ ] Resume analytics and tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.