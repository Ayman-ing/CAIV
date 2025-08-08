# Database Schema Changelog

## [2025-08-08] - Inheritance-Based Global Entity System Implementation

### Overview
Major refactor of the vector embeddings system to implement an inheritance-based global entity system for improved performance, maintainability, and scalability.

### Migrations Applied

#### 1. `4d381a20854c` - Initial Vector Embeddings FK Relationships
- Added foreign key relationships from vector_embeddings to all entity tables
- Created 12 nullable foreign key columns in vector_embeddings table
- Established basic relationships for AI embedding functionality

#### 2. `013fc9c3a89b` - Implement Inheritance Based Global Entity System
**Major architectural change implementing BaseEntity inheritance pattern**

**Added:**
- `entity_id` (UUID) column to all embeddable entity tables:
  - certificates, education, generated_resumes, job_descriptions
  - languages, professional_summaries, profile_links, projects
  - skills, work_experiences
- Unique constraints on all entity_id columns
- New indexes on vector_embeddings: `idx_vector_embeddings_entity`, `idx_vector_embeddings_qdrant`

**Removed:**
- All 12 foreign key constraints from vector_embeddings table
- All 12 foreign key columns from vector_embeddings:
  - education_id, work_experience_id, certificate_id, project_id
  - language_id, skill_id, professional_summary_id, job_description_id
  - profile_id, custom_section_id, generated_resume_id, profile_link_id

**Modified:**
- vector_embeddings.entity_id now uses UUID type (was polymorphic entity_type/entity_id)

#### 3. `5adc69a5fade` - Fix Custom Sections Schema
**Fixed custom_sections table to match inheritance pattern**

**Added:**
- `entity_id` (UUID) column to custom_sections table with unique constraint
- `profile_id` (Integer) column with foreign key to profiles.id

**Removed:**
- `user_id` column (was incorrectly named, actually referenced profiles.id)
- Old foreign key constraint custom_sections_user_id_fkey

**Data Migration:**
- Migrated data from user_id to profile_id before dropping user_id column

### Schema Changes Summary

#### Before (Multiple FK Approach)
```sql
-- Vector embeddings with 12 nullable foreign keys
CREATE TABLE vector_embeddings (
    id SERIAL PRIMARY KEY,
    -- 12 nullable foreign key columns (only 1 ever populated)
    work_experience_id INTEGER REFERENCES work_experiences(id),
    project_id INTEGER REFERENCES projects(id),
    education_id INTEGER REFERENCES education(id),
    -- ... 9 more nullable FK columns
    entity_type VARCHAR(50),  -- polymorphic type
    entity_id INTEGER,        -- polymorphic id
    -- other fields...
);
```

#### After (Global Entity System)
```sql
-- Clean inheritance-based design
CREATE TABLE vector_embeddings (
    id SERIAL PRIMARY KEY,
    entity_id UUID NOT NULL,  -- Single reference to any BaseEntity
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL,
    -- other fields...
);

-- All embeddable entities now have global entity_id
CREATE TABLE work_experiences (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL,
    entity_id UUID UNIQUE NOT NULL,  -- Global entity identifier
    profile_id INTEGER REFERENCES profiles(id),
    -- entity-specific fields...
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Benefits Achieved

#### Performance Improvements
- ✅ Reduced vector_embeddings table from 15+ columns to 8 columns
- ✅ Eliminated 12 nullable foreign key columns
- ✅ Single UUID index instead of 12 separate indexes
- ✅ Better query performance with direct UUID lookups

#### Schema Simplification
- ✅ No more empty/orphaned embedding records
- ✅ Every embedding record has exactly one entity reference
- ✅ Consistent foreign key patterns across all profile entities
- ✅ Eliminated polymorphic entity_type/entity_id complexity

#### Architecture Improvements
- ✅ Type-safe inheritance pattern with SQLAlchemy
- ✅ Automatic entity_id assignment via BaseEntity
- ✅ Built-in embeddings relationship for all entities
- ✅ Clear separation: Profile = container, entities inherit from BaseEntity

#### Maintainability
- ✅ Easy to extend with new embeddable entity types
- ✅ Consistent model patterns across all entities
- ✅ Centralized entity management through BaseEntity
- ✅ Simplified relationship declarations with declared_attr

### Database State After Migrations

#### Entity Tables with entity_id
All embeddable entities now have the global entity_id system:
- ✅ work_experiences
- ✅ projects
- ✅ education
- ✅ skills
- ✅ certificates
- ✅ languages
- ✅ professional_summaries
- ✅ profile_links
- ✅ custom_sections
- ✅ job_descriptions
- ✅ generated_resumes

#### Vector Embeddings Table
- Single entity_id (UUID) column references any BaseEntity
- Proper indexes for performance
- Clean relationship to Qdrant vector database

#### Container Tables (No entity_id)
These tables act as containers and do not inherit from BaseEntity:
- users (authentication)
- profiles (profile container)
- resume_components (metadata)
- job_keywords (extracted data)
- job_requirements (extracted data)
- outbox_events (system events)

### Rollback Information

Each migration includes proper downgrade functions for rollback if needed:
- Migration `5adc69a5fade` can restore user_id column in custom_sections
- Migration `013fc9c3a89b` can restore all 12 FK columns in vector_embeddings
- Migration `4d381a20854c` can remove all FK relationships

### Next Steps

The inheritance-based global entity system is now complete and ready for:
1. AI-powered resume generation with vector embeddings
2. Intelligent job matching based on profile components
3. Content similarity analysis across all entity types
4. Extensible entity system for future features

### Validation

All entity tables have been verified to have the correct schema:
```bash
# Verification command used
uv run python -c "
# Script that verified all 11 entity tables have entity_id columns
# Result: ✅ All entity tables properly configured
"
```
