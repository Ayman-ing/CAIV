# Global Entity ID System for Vector Embeddings

## The Problem
Currently, vector_embeddings has 12 nullable foreign key columns, resulting in mostly empty columns per row.

## Solution: Global Entity ID System

### Step 1: Create Central Entities Table
```sql
CREATE TABLE entities (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    entity_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Ensure one record per entity
    UNIQUE(table_name, record_id)
);
```

### Step 2: Add entity_id to All Tables
```sql
-- Add to all entity tables
ALTER TABLE profiles ADD COLUMN entity_id INTEGER UNIQUE REFERENCES entities(id);
ALTER TABLE projects ADD COLUMN entity_id INTEGER UNIQUE REFERENCES entities(id);
ALTER TABLE work_experiences ADD COLUMN entity_id INTEGER UNIQUE REFERENCES entities(id);
ALTER TABLE education ADD COLUMN entity_id INTEGER UNIQUE REFERENCES entities(id);
-- etc. for all tables
```

### Step 3: Simplified Vector Embeddings
```sql
-- Clean vector_embeddings table
CREATE TABLE vector_embeddings (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    entity_id INTEGER NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    qdrant_point_id UUID UNIQUE NOT NULL,
    embedding_type VARCHAR(50) NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Benefits
1. ✅ **No nullable columns** - Every embedding references exactly one entity
2. ✅ **Single source of truth** - All entities have a global unique ID
3. ✅ **Referential integrity** - Direct foreign key relationships
4. ✅ **Extensible** - Easy to add new entity types
5. ✅ **Clean queries** - Simple joins through entity_id

## Usage Examples

```python
# Get entity for a project
project = session.query(Project).first()
entity = project.entity  # Access through relationship

# Get all embeddings for this entity
embeddings = entity.embeddings

# Or directly from project
embeddings = project.embeddings  # Through entity relationship

# Find source entity for an embedding
embedding = session.query(VectorEmbedding).first()
source_entity = embedding.entity
actual_record = getattr(source_entity, source_entity.table_name.rstrip('s'))  # Get actual record
```
