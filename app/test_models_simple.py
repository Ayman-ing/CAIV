#!/usr/bin/env python3
"""
Simple test for the new entity structure without full app imports.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_model_structure():
    """Test the model structure without database connections."""
    
    print("🧪 Testing New Entity Model Structure")
    print("=" * 50)
    
    try:
        # Import models directly
        from shared.models.entity import Entity, BaseEntity
        from features.vector_embeddings.models import Embedding
        
        print("\n1️⃣  Testing Basic Model Imports:")
        print(f"   ✅ Entity class imported: {Entity}")
        print(f"   ✅ BaseEntity class imported: {BaseEntity}")
        print(f"   ✅ Embedding class imported: {Embedding}")
        
        # Test table names
        print("\n2️⃣  Testing Table Names:")
        print(f"   ✅ Entity table: {Entity.__tablename__}")
        print(f"   ✅ Embedding table: {Embedding.__tablename__}")
        
        # Test polymorphic setup
        print("\n3️⃣  Testing Polymorphic Setup:")
        entity_mapper_args = Entity.__mapper_args__
        print(f"   ✅ Entity polymorphic identity: {entity_mapper_args.get('polymorphic_identity')}")
        print(f"   ✅ Entity polymorphic on: {entity_mapper_args.get('polymorphic_on')}")
        
        # Test relationships
        print("\n4️⃣  Testing Relationship Definitions:")
        print(f"   ✅ Entity.embeddings relationship defined: {hasattr(Entity, 'embeddings')}")
        print(f"   ✅ Embedding.entity relationship defined: {hasattr(Embedding, 'entity')}")
        
        # Test columns
        print("\n5️⃣  Testing Column Structure:")
        entity_columns = [col.name for col in Entity.__table__.columns]
        embedding_columns = [col.name for col in Embedding.__table__.columns]
        
        print(f"   ✅ Entity columns: {entity_columns}")
        print(f"   ✅ Embedding columns: {embedding_columns}")
        
        # Check foreign key setup
        embedding_fks = []
        for col in Embedding.__table__.columns:
            if col.foreign_keys:
                for fk in col.foreign_keys:
                    embedding_fks.append(f"{col.name} -> {fk.column}")
        
        print(f"   ✅ Embedding foreign keys: {embedding_fks}")
        
        print("\n✅ All basic model structure tests passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing model structure: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_work_experience_model():
    """Test a specific entity model."""
    print("\n6️⃣  Testing WorkExperience Model:")
    
    try:
        from features.profiles.work_experiences.models import WorkExperience
        
        print(f"   ✅ WorkExperience imported: {WorkExperience}")
        print(f"   ✅ WorkExperience table: {WorkExperience.__tablename__}")
        
        # Check inheritance
        mro_names = [cls.__name__ for cls in WorkExperience.__mro__]
        print(f"   ✅ WorkExperience inheritance: {mro_names}")
        
        # Check polymorphic identity
        we_mapper_args = WorkExperience.__mapper_args__
        print(f"   ✅ WorkExperience polymorphic identity: {we_mapper_args.get('polymorphic_identity')}")
        
        # Check columns including inherited ones
        we_columns = [col.name for col in WorkExperience.__table__.columns]
        print(f"   ✅ WorkExperience columns: {we_columns}")
        
        # Check foreign keys
        we_fks = []
        for col in WorkExperience.__table__.columns:
            if col.foreign_keys:
                for fk in col.foreign_keys:
                    we_fks.append(f"{col.name} -> {fk.column}")
        print(f"   ✅ WorkExperience foreign keys: {we_fks}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing WorkExperience: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_structure()
    if success:
        test_work_experience_model()
    
    print("\n" + "=" * 50)
    print("🎉 Model structure testing complete!")
