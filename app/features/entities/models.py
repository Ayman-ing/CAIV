# This file is no longer needed as BaseEntity has been moved to shared/models/entity.py
# and simplified to use proper table inheritance with the Entity table.
# 
# All entities now inherit from BaseEntity which inherits from Entity table,
# providing clean foreign key relationships to the embeddings table.

# Import for backward compatibility if needed
from shared.models.entity import Entity, BaseEntity