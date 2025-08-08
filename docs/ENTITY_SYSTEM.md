# Inheritance-Based Global Entity System

## Overview

The AI Resume Builder implements a sophisticated inheritance-based global entity system to manage vector embeddings and provide a clean, scalable architecture for AI-powered features.

## Architecture

### Core Components

#### 1. BaseEntity Abstract Class

Located: `app/shared/models/entity.py`

```python
class BaseEntity(Base):
    """Base class for all entities that can have vector embeddings."""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), unique=True, nullable=False)  # Global identifier
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    @declared_attr
    def embeddings(cls):
        return relationship("VectorEmbedding", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.entity_id:
            self.entity_id = uuid.uuid4()
    
    @property
    def entity_type(self):
        return self.__tablename__
```

#### 2. Entity Types

**Container Entity**:
- `profiles` - Does NOT inherit from BaseEntity
- Acts as a container for embeddable entities
- Has relationships to all profile components

**Embeddable Entities** (inherit from BaseEntity):
- Profile Components:
  - `work_experiences`
  - `projects`
  - `education`
  - `skills`
  - `certificates`
  - `languages`
  - `professional_summaries`
  - `profile_links`
  - `custom_sections`
- Main Entities:
  - `job_descriptions`
  - `generated_resumes`

#### 3. Vector Embedding System

Located: `app/features/vector_embeddings/models.py`

```python
class VectorEmbedding(Base):
    __tablename__ = 'vector_embeddings'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    qdrant_point_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    
    # Global entity reference using the global entity_id from BaseEntity
    entity_id = Column(UUID(as_uuid=True), nullable=False)  # References BaseEntity.entity_id
    
    embedding_type = Column(String(50), nullable=False)  # 'full_text', 'summary', 'keywords'
    chunk_index = Column(Integer, default=0)  # For chunked content
    metadata_json = Column(Text)  # JSON metadata about the embedding
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
```

## Benefits

### 1. Simplified Schema

**Before** (Multiple FK approach):
```sql
CREATE TABLE vector_embeddings (
    id SERIAL PRIMARY KEY,
    work_experience_id INTEGER,      -- nullable
    project_id INTEGER,              -- nullable
    education_id INTEGER,            -- nullable
    skill_id INTEGER,                -- nullable
    certificate_id INTEGER,          -- nullable
    language_id INTEGER,             -- nullable
    professional_summary_id INTEGER, -- nullable
    profile_link_id INTEGER,         -- nullable
    custom_section_id INTEGER,       -- nullable
    job_description_id INTEGER,      -- nullable
    generated_resume_id INTEGER,     -- nullable
    profile_id INTEGER,              -- nullable
    -- 12 nullable columns with only 1 ever populated!
);
```

**After** (Global entity system):
```sql
CREATE TABLE vector_embeddings (
    id SERIAL PRIMARY KEY,
    entity_id UUID NOT NULL,  -- References any BaseEntity.entity_id
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2. Performance Improvements

- **Single Index**: One UUID index instead of 12 separate indexes
- **No Nullable Columns**: Every record has exactly one entity reference
- **Better Query Performance**: Direct UUID lookups instead of complex OR conditions
- **Reduced Storage**: Eliminated 11 nullable integer columns per row

### 3. Maintainability

- **Type Safety**: SQLAlchemy inheritance provides compile-time checking
- **Consistent Pattern**: All embeddable entities follow the same inheritance pattern
- **Easy Extension**: Adding new embeddable entity types is straightforward
- **Clear Separation**: Profile is container, entities inherit from BaseEntity

### 4. Scalability

- **Global Identification**: Unique entity_id across all entity types
- **Clean Relationships**: No orphaned or ambiguous references
- **Extensible**: Easy to add new entity types without schema changes

## Implementation Details

### Database Migrations

The system was implemented through a series of migrations:

1. **`4d381a20854c`** - Initial approach with foreign key relationships
2. **`013fc9c3a89b`** - Major refactor to inheritance-based global entity system
3. **`5adc69a5fade`** - Fixed custom_sections table schema

### Relationship Patterns

All embeddable entities use `declared_attr` for proper inheritance:

```python
class WorkExperience(BaseEntity):
    __tablename__ = 'work_experiences'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    job_title = Column(String)
    company = Column(String)
    # ... other fields
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="work_experiences")
    # embeddings relationship is inherited from BaseEntity
```

### Automatic Entity ID Assignment

BaseEntity automatically assigns a unique UUID to each entity:

```python
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    if not self.entity_id:
        self.entity_id = uuid.uuid4()  # Global unique identifier
```

## Usage Examples

### Creating an Entity with Embeddings

```python
# Create a work experience (automatically gets entity_id)
work_exp = WorkExperience(
    profile_id=profile.id,
    job_title="Software Engineer",
    company="Tech Corp"
)
session.add(work_exp)
session.commit()

# Entity automatically has global entity_id
print(work_exp.entity_id)  # UUID like: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'

# Create vector embedding for this entity
embedding = VectorEmbedding(
    entity_id=work_exp.entity_id,  # References the global entity_id
    qdrant_point_id=uuid.uuid4(),
    embedding_type="full_text"
)
session.add(embedding)
session.commit()

# Access embeddings through relationship
embeddings = work_exp.embeddings  # List of VectorEmbedding objects
```

### Querying Entities and Embeddings

```python
# Find all embeddings for a specific entity
embeddings = session.query(VectorEmbedding).filter(
    VectorEmbedding.entity_id == work_exp.entity_id
).all()

# Find entity by embedding
embedding = session.query(VectorEmbedding).first()
# Can determine entity type from the entity_id and query appropriate table

# Get all entities with embeddings (polymorphic query would require joins)
# With global system, can efficiently track all embedded entities
```

## Future Enhancements

1. **Entity Type Registry**: Maintain a registry of all entity types for dynamic queries
2. **Metadata Tracking**: Store entity type information in embeddings metadata
3. **Cascade Operations**: Implement cascading operations across entity relationships
4. **Audit Trail**: Track changes to entities through the global entity system

## Migration Guide

If extending the system with new embeddable entities:

1. **Inherit from BaseEntity**:
   ```python
   class NewEntity(BaseEntity):
       __tablename__ = 'new_entities'
       # fields...
   ```

2. **Use declared_attr for relationships**:
   ```python
   @declared_attr
   def parent(cls):
       return relationship("Parent", back_populates="new_entities")
   ```

3. **Generate migration**:
   ```bash
   uv run alembic revision --autogenerate -m "add new entity type"
   uv run alembic upgrade head
   ```

The inheritance system will automatically provide entity_id and embeddings relationship.
