import os
import re

def fix_blockquote_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix closing blockquote tag
        original = content
        content = content.replace('</blockquote>', '</blockquote>')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

# Find all Python files
fixed_count = 0
for root, dirs, files in os.walk('.'):
    # Skip hidden and unwanted directories
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'node_modules']]
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            if fix_blockquote_in_file(filepath):
                print(f"Fixed: {filepath}")
                fixed_count += 1

print(f"\nTotal files fixed: {fixed_count}")
