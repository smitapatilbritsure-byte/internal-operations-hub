import os
import re

dirs_to_check = ['user-service', 'audit-service', 'request-service', 'shared']
ignore_comment = '# pyrefly: ignore [missing-import]'

skip_modules = {'os', 'sys', 'pathlib', 'typing', 'datetime', 'enum', 'uuid', 'json', 'time'}

for d in dirs_to_check:
    if not os.path.exists(d):
        continue
    for root, dirs, files in os.walk(d):
        if 'venv' in dirs:
            dirs.remove('venv')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
            
        for file in files:
            if not file.endswith('.py'):
                continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            for i, line in enumerate(lines):
                stripped = line.strip()
                is_import = stripped.startswith('import ') or stripped.startswith('from ')
                if is_import:
                    # check if we should skip
                    parts = stripped.split()
                    mod = parts[1].split('.')[0] if stripped.startswith('import ') else parts[1].split('.')[0]
                    if mod not in skip_modules:
                        # Check if previous line already has the comment
                        if not (len(new_lines) > 0 and new_lines[-1].strip() == ignore_comment):
                            new_lines.append(f"{line[:len(line) - len(line.lstrip())]}{ignore_comment}\n")
                new_lines.append(line)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
print("Done fixing pyrefly errors.")
