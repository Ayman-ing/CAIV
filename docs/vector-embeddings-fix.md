# Vector Embeddings Relationship Improvements

## Current Problem

The `vector_embeddings` table uses a generic polymorphic pattern that lacks proper foreign key relationships:

```sql
-- Current problematic structure
CREATE TABLE vector_embeddings (
    id INTEGER PRIMARY KEY,
    entity_type STRING,  -- 'profile', 'job_description', etc.
    entity_id INTEGER,   -- No foreign key constraint
    qdrant_point_id UUID
);
```

This creates data integrity issues and poor performance.

## Solution 1: Separate Embedding Tables (Recommended)

Replace the single `vector_embeddings` table with specific embedding tables for each entity type:

```sql
-- Profile embeddings
CREATE TABLE profile_embeddings (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL, -- 'full_profile', 'summary', 'skills'
    chunk_index INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Job description embeddings
CREATE TABLE job_description_embeddings (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    job_description_id INTEGER NOT NULL REFERENCES job_descriptions(id) ON DELETE CASCADE,
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL, -- 'full_description', 'requirements', 'keywords'
    chunk_index INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Resume embeddings
CREATE TABLE resume_embeddings (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    generated_resume_id INTEGER NOT NULL REFERENCES generated_resumes(id) ON DELETE CASCADE,
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL, -- 'full_resume', 'summary', 'experience'
    chunk_index INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Work experience embeddings (for detailed matching)
CREATE TABLE work_experience_embeddings (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    work_experience_id INTEGER NOT NULL REFERENCES work_experiences(id) ON DELETE CASCADE,
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL, -- 'full_experience', 'description', 'skills_used'
    chunk_index INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Project embeddings
CREATE TABLE project_embeddings (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL, -- 'full_project', 'description', 'technologies'
    chunk_index INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Benefits:
- ✅ **Proper foreign key relationships**
- ✅ **Referential integrity with CASCADE deletes**
- ✅ **Better query performance with direct joins**
- ✅ **Type-safe relationships**
- ✅ **Clear data lineage**

### Indexes for Performance:
```sql
-- Profile embeddings indexes
CREATE INDEX idx_profile_embeddings_profile_id ON profile_embeddings(profile_id);
CREATE INDEX idx_profile_embeddings_qdrant_id ON profile_embeddings(qdrant_point_id);
CREATE INDEX idx_profile_embeddings_type ON profile_embeddings(embedding_type);

-- Job description embeddings indexes
CREATE INDEX idx_job_description_embeddings_job_id ON job_description_embeddings(job_description_id);
CREATE INDEX idx_job_description_embeddings_qdrant_id ON job_description_embeddings(qdrant_point_id);
CREATE INDEX idx_job_description_embeddings_type ON job_description_embeddings(embedding_type);

-- Resume embeddings indexes
CREATE INDEX idx_resume_embeddings_resume_id ON resume_embeddings(generated_resume_id);
CREATE INDEX idx_resume_embeddings_qdrant_id ON resume_embeddings(qdrant_point_id);

-- Work experience embeddings indexes
CREATE INDEX idx_work_experience_embeddings_work_id ON work_experience_embeddings(work_experience_id);
CREATE INDEX idx_work_experience_embeddings_qdrant_id ON work_experience_embeddings(qdrant_point_id);

-- Project embeddings indexes
CREATE INDEX idx_project_embeddings_project_id ON project_embeddings(project_id);
CREATE INDEX idx_project_embeddings_qdrant_id ON project_embeddings(qdrant_point_id);
```

## Solution 2: Improved Polymorphic with Constraints

If you prefer to keep a single table, add proper constraints:

```sql
-- Drop current vector_embeddings table
DROP TABLE vector_embeddings;

-- Create improved polymorphic table
CREATE TABLE vector_embeddings (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraint to ensure entity_type is valid
    CONSTRAINT chk_entity_type CHECK (entity_type IN (
        'profile', 'job_description', 'generated_resume', 
        'work_experience', 'project', 'education', 'skill'
    ))
);

-- Create partial indexes for each entity type (better performance)
CREATE INDEX idx_vector_embeddings_profile 
    ON vector_embeddings(entity_id) 
    WHERE entity_type = 'profile';

CREATE INDEX idx_vector_embeddings_job_description 
    ON vector_embeddings(entity_id) 
    WHERE entity_type = 'job_description';

CREATE INDEX idx_vector_embeddings_resume 
    ON vector_embeddings(entity_id) 
    WHERE entity_type = 'generated_resume';

CREATE INDEX idx_vector_embeddings_work_experience 
    ON vector_embeddings(entity_id) 
    WHERE entity_type = 'work_experience';

CREATE INDEX idx_vector_embeddings_project 
    ON vector_embeddings(entity_id) 
    WHERE entity_type = 'project';

-- Index for Qdrant lookups
CREATE INDEX idx_vector_embeddings_qdrant_id ON vector_embeddings(qdrant_point_id);
CREATE INDEX idx_vector_embeddings_type ON vector_embeddings(embedding_type);
```

### Add referential integrity through triggers:
```sql
-- Function to validate entity exists
CREATE OR REPLACE FUNCTION validate_vector_embedding_entity()
RETURNS TRIGGER AS $$
BEGIN
    -- Validate that the referenced entity exists
    IF NEW.entity_type = 'profile' THEN
        IF NOT EXISTS (SELECT 1 FROM profiles WHERE id = NEW.entity_id) THEN
            RAISE EXCEPTION 'Profile with id % does not exist', NEW.entity_id;
        END IF;
    ELSIF NEW.entity_type = 'job_description' THEN
        IF NOT EXISTS (SELECT 1 FROM job_descriptions WHERE id = NEW.entity_id) THEN
            RAISE EXCEPTION 'Job description with id % does not exist', NEW.entity_id;
        END IF;
    ELSIF NEW.entity_type = 'generated_resume' THEN
        IF NOT EXISTS (SELECT 1 FROM generated_resumes WHERE id = NEW.entity_id) THEN
            RAISE EXCEPTION 'Generated resume with id % does not exist', NEW.entity_id;
        END IF;
    ELSIF NEW.entity_type = 'work_experience' THEN
        IF NOT EXISTS (SELECT 1 FROM work_experiences WHERE id = NEW.entity_id) THEN
            RAISE EXCEPTION 'Work experience with id % does not exist', NEW.entity_id;
        END IF;
    ELSIF NEW.entity_type = 'project' THEN
        IF NOT EXISTS (SELECT 1 FROM projects WHERE id = NEW.entity_id) THEN
            RAISE EXCEPTION 'Project with id % does not exist', NEW.entity_id;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER trg_validate_vector_embedding_entity
    BEFORE INSERT OR UPDATE ON vector_embeddings
    FOR EACH ROW EXECUTE FUNCTION validate_vector_embedding_entity();
```

## Recommended Approach: Solution 1

I strongly recommend **Solution 1 (Separate Tables)** because:

1. **Better Performance**: Direct foreign key joins are much faster than polymorphic queries
2. **Data Integrity**: Built-in foreign key constraints prevent orphaned embeddings
3. **Clearer Schema**: Each table has a clear, specific purpose
4. **Better Tooling Support**: ORMs and database tools work better with proper relationships
5. **Easier Maintenance**: Simpler to manage and understand

## Migration Strategy

Here's how to migrate from the current structure to the new one:

```sql
-- Step 1: Create new embedding tables
-- (Run the CREATE TABLE statements from Solution 1)

-- Step 2: Migrate existing data
INSERT INTO profile_embeddings (profile_id, qdrant_point_id, embedding_type, chunk_index, metadata_json, created_at, updated_at)
SELECT entity_id, qdrant_point_id, 'full_profile', chunk_index, metadata_json, created_at, updated_at
FROM vector_embeddings 
WHERE entity_type = 'profile';

INSERT INTO job_description_embeddings (job_description_id, qdrant_point_id, embedding_type, chunk_index, metadata_json, created_at, updated_at)
SELECT entity_id, qdrant_point_id, 'full_description', chunk_index, metadata_json, created_at, updated_at
FROM vector_embeddings 
WHERE entity_type = 'job_description';

-- Continue for other entity types...

-- Step 3: Update application code to use new tables

-- Step 4: Drop old table
DROP TABLE vector_embeddings;
```

## Updated Model Relationships

With the new structure, your SQLAlchemy models would have proper relationships:

```python
# In profiles/models.py
class Profile(Base):
    # ... existing fields ...
    embeddings = relationship("ProfileEmbedding", back_populates="profile", cascade="all, delete-orphan")

# In job_descriptions/models.py  
class JobDescription(Base):
    # ... existing fields ...
    embeddings = relationship("JobDescriptionEmbedding", back_populates="job_description", cascade="all, delete-orphan")

# New embedding models
class ProfileEmbedding(Base):
    __tablename__ = 'profile_embeddings'
    # ... fields ...
    profile = relationship("Profile", back_populates="embeddings")

class JobDescriptionEmbedding(Base):
    __tablename__ = 'job_description_embeddings'
    # ... fields ...
    job_description = relationship("JobDescription", back_populates="embeddings")
```

This gives you proper type-safe relationships and much better query capabilities!
