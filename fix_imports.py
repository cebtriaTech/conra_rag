import os

REPLACEMENTS = {
    'from ask import': 'from services.rag import',
    'import ask': 'import services.rag',
    'from download_model import': 'from services.embedder import',
    'import download_model': 'import services.embedder',
    'from services.qdrant_client import': 'from services.qdrant_client import',
    'import qdrant_client': 'import services.qdrant_client',
}

def update_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    new_lines = []

    for line in lines:
        for old, new in REPLACEMENTS.items():
            if old in line:
                line = line.replace(old, new)
                modified = True
        new_lines.append(line)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"✅ Updated imports in: {file_path}")

def walk_and_fix(start_dir):
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.py') and file != 'fix_imports.py':
                update_imports(os.path.join(root, file))

if __name__ == '__main__':
    walk_and_fix('.')
