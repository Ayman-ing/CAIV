#!/usr/bin/env python3
"""
Script to update all BaseEntity subclasses to use proper joined table inheritance.
"""

import os
import re
from pathlib import Path

def update_entity_model(file_path, class_name, table_name):
    """Update a single entity model file."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove declared_attr import if present
    content = re.sub(r', declared_attr', '', content)
    content = re.sub(r'from sqlalchemy.orm import relationship, declared_attr', 
                     'from sqlalchemy.orm import relationship', content)
    content = re.sub(r'from sqlalchemy.orm import declared_attr, relationship', 
                     'from sqlalchemy.orm import relationship', content)
    
    # Find the class definition and update it
    class_pattern = rf'class {class_name}\(BaseEntity\):\s*\n\s*__tablename__ = [\'\"]{table_name}[\'\"]\s*\n'
    
    replacement = f'''class {class_name}(BaseEntity):
    __tablename__ = '{table_name}'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # {class_name} specific fields
'''
    
    content = re.sub(class_pattern, replacement, content)
    
    # Remove @declared_attr decorators and fix relationships
    content = re.sub(r'\s*@declared_attr\s*\n\s*def (\w+)\(cls\):\s*\n\s*return relationship\((.*?)\)', 
                     r'    # Relationships\n    \1 = relationship(\2)', content)
    
    # Add polymorphic identity and mapper args
    polymorphic_identity = table_name.rstrip('s')  # Remove trailing 's' for identity
    if polymorphic_identity == 'education':  # Special case
        polymorphic_identity = 'education'
    elif polymorphic_identity == 'work_experience':  # Special case
        polymorphic_identity = 'work_experience'
    else:
        polymorphic_identity = table_name.rstrip('s')
    
    # Add mapper args before the last line if not already present
    if '__mapper_args__' not in content:
        # Find the end of the class
        lines = content.split('\n')
        insert_pos = len(lines) - 1
        
        # Find the last non-empty line of the class
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() and not lines[i].startswith('class ') and lines[i].startswith('    '):
                insert_pos = i + 1
                break
        
        mapper_args = f'''    
    __mapper_args__ = {{
        'polymorphic_identity': '{polymorphic_identity}',
    }}'''
        
        lines.insert(insert_pos, mapper_args)
        content = '\n'.join(lines)
    
    # Write back the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {class_name} in {file_path}")

def main():
    """Update all entity models."""
    
    base_path = Path(".")
    
    # List of models to update (excluding the ones we already fixed)
    models_to_update = [
        ("features/profiles/languages/models.py", "Language", "languages"),
        ("features/profiles/profile_links/models.py", "ProfileLink", "profile_links"),
        ("features/profiles/custom_sections/models.py", "CustomSection", "custom_sections"),
        ("features/profiles/certificates/models.py", "Certificate", "certificates"),
        ("features/profiles/professional_summaries/models.py", "ProfessionalSummary", "professional_summaries"),
        ("features/resumes/models.py", "GeneratedResume", "generated_resumes"),
        ("features/job_descriptions/models.py", "JobDescription", "job_descriptions"),
    ]
    
    for file_path, class_name, table_name in models_to_update:
        full_path = base_path / file_path
        if full_path.exists():
            try:
                update_entity_model(full_path, class_name, table_name)
            except Exception as e:
                print(f"❌ Error updating {class_name}: {e}")
        else:
            print(f"⚠️  File not found: {full_path}")

if __name__ == "__main__":
    main()
