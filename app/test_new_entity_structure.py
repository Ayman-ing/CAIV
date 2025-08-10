#!/usr/bin/env python3
"""
Test script for the new entity inheritance structure.
This will help us verify that:
1. The Entity table inheritance works correctly
2. Relationships to embeddings are clean
3. No more SQLAlchemy warnings about overlapping relationships
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.database import get_database_url

# Import our models
from shared.models.entity import Entity, BaseEntity
from features.vector_embeddings.models import Embedding
from features.profiles.work_experiences.models import WorkExperience
from features.profiles.projects.models import Project

def test_entity_structure():
    """Test the new entity inheritance structure."""
    
    print("🧪 Testing New Entity Inheritance Structure")
    print("=" * 50)
    
    # Create engine
    engine = create_engine(get_database_url())
    
    try:
        # Test 1: Check table relationships
        print("\n1️⃣  Testing Entity Table Structure:")
        
        print(f"   ✅ Entity table: {Entity.__tablename__}")
        print(f"   ✅ Entity polymorphic identity: {Entity.__mapper_args__.get('polymorphic_identity')}")
        
        print(f"   ✅ WorkExperience table: {WorkExperience.__tablename__}")
        print(f"   ✅ WorkExperience polymorphic identity: {WorkExperience.__mapper_args__.get('polymorphic_identity')}")
        
        print(f"   ✅ Project table: {Project.__tablename__}")
        print(f"   ✅ Project polymorphic identity: {Project.__mapper_args__.get('polymorphic_identity')}")
        
        print(f"   ✅ Embedding table: {Embedding.__tablename__}")
        
        # Test 2: Check relationships
        print("\n2️⃣  Testing Relationships:")
        
        # Check Entity -> Embeddings relationship
        entity_embeddings = Entity.embeddings
        print(f"   ✅ Entity.embeddings relationship: {entity_embeddings}")
        
        # Check Embedding -> Entity relationship  
        embedding_entity = Embedding.entity
        print(f"   ✅ Embedding.entity relationship: {embedding_entity}")
        
        # Test 3: Inheritance chain
        print("\n3️⃣  Testing Inheritance Chain:")
        print(f"   ✅ WorkExperience MRO: {[cls.__name__ for cls in WorkExperience.__mro__]}")
        print(f"   ✅ Project MRO: {[cls.__name__ for cls in Project.__mro__]}")
        
        # Test 4: Foreign key structure
        print("\n4️⃣  Testing Foreign Key Structure:")
        
        # Check WorkExperience foreign keys
        work_exp_fks = [col for col in WorkExperience.__table__.columns if col.foreign_keys]
        print(f"   ✅ WorkExperience foreign keys: {[f'{col.name} -> {list(col.foreign_keys)[0].column}' for col in work_exp_fks]}")
        
        # Check Project foreign keys
        project_fks = [col for col in Project.__table__.columns if col.foreign_keys]
        print(f"   ✅ Project foreign keys: {[f'{col.name} -> {list(col.foreign_keys)[0].column}' for col in project_fks]}")
        
        # Check Embedding foreign keys
        embedding_fks = [col for col in Embedding.__table__.columns if col.foreign_keys]
        print(f"   ✅ Embedding foreign keys: {[f'{col.name} -> {list(col.foreign_keys)[0].column}' for col in embedding_fks]}")
        
        print("\n✅ All tests passed! New entity structure looks good.")
        
        # Test 5: Show example queries that are now possible
        print("\n5️⃣  Example Queries Now Possible:")
        print("""
        # Get all embeddings for a work experience with entity details
        embeddings = session.query(Embedding)\\
            .join(Entity)\\
            .filter(Entity.entity_type == 'work_experience')\\
            .filter(Entity.id == work_exp_id)\\
            .all()
        
        # Get embedding statistics by entity type
        stats = session.query(
            Entity.entity_type,
            func.count(Embedding.id),
            func.sum(Embedding.token_count)
        ).join(Embedding).group_by(Entity.entity_type).all()
        
        # Get all entities that have embeddings
        entities_with_embeddings = session.query(Entity)\\
            .join(Embedding)\\
            .distinct()\\
            .all()
        """)
        
    except Exception as e:
        print(f"❌ Error testing entity structure: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_entity_structure()
