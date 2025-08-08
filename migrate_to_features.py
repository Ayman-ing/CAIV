#!/usr/bin/env python3
"""
Migration script to help transition from old layered architecture to new feature-based architecture.
This script will help identify remaining models and create the feature structure.
"""

import os
from pathlib import Path

# Define the features based on existing models
FEATURE_MAPPING = {
    "users": ["user", "user_link"],
    "work_experiences": ["work_experience"],
    "education": ["education"],
    "skills": ["skill"],
    "projects": ["project"],
    "certificates": ["certificate"],
    "languages": ["language"],
    "resumes": ["generated_resume", "resume_component"],
    "job_matching": ["job_description", "job_keyword", "job_requirement"],
    "profiles": ["professional_summary", "custom_section"],
    "system": ["outbox_event", "vector_embedding"]
}

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent

def list_old_models():
    """List all models in the old db/models directory"""
    old_models_dir = get_project_root() / "app" / "db" / "models"
    if not old_models_dir.exists():
        print("Old models directory not found!")
        return []
    
    models = []
    for file in old_models_dir.glob("*.py"):
        if file.name != "__init__.py":
            models.append(file.stem)
    
    return models

def list_existing_features():
    """List existing features"""
    features_dir = get_project_root() / "app" / "features"
    if not features_dir.exists():
        return []
    
    features = []
    for dir in features_dir.iterdir():
        if dir.is_dir() and not dir.name.startswith("_"):
            features.append(dir.name)
    
    return features

def suggest_migration_plan():
    """Suggest what needs to be migrated"""
    old_models = list_old_models()
    existing_features = list_existing_features()
    
    print("=== MIGRATION STATUS ===")
    print(f"Old models found: {old_models}")
    print(f"Existing features: {existing_features}")
    print()
    
    # Find models that haven't been migrated
    migrated_models = set()
    for feature in existing_features:
        if feature in FEATURE_MAPPING:
            migrated_models.update(FEATURE_MAPPING[feature])
    
    remaining_models = set(old_models) - migrated_models
    
    print("=== REMAINING MODELS TO MIGRATE ===")
    for model in remaining_models:
        # Find which feature this model belongs to
        target_feature = None
        for feature, models in FEATURE_MAPPING.items():
            if model in models:
                target_feature = feature
                break
        
        if target_feature:
            print(f"  {model}.py → features/{target_feature}/")
        else:
            print(f"  {model}.py → [NEEDS CLASSIFICATION]")
    
    print()
    print("=== RECOMMENDED NEXT STEPS ===")
    for feature, models in FEATURE_MAPPING.items():
        if feature not in existing_features and any(model in old_models for model in models):
            needed_models = [m for m in models if m in old_models]
            print(f"  Create feature '{feature}' with models: {needed_models}")

if __name__ == "__main__":
    suggest_migration_plan()
