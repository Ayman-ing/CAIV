import os
import re

# Fix all model imports
for root, dirs, files in os.walk('app/features'):
    for file in files:
        if file == 'models.py':
            filepath = os.path.join(root, file)
            print(f'Fixing {filepath}')
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Replace app.shared.models.base with shared.models.base
            content = content.replace('from shared.models.base import Base', 'from shared.models.base import Base')
            
            with open(filepath, 'w') as f:
                f.write(content)

print('✅ Fixed all model imports')
