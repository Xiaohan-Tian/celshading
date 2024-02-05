import re

file_path = "src/__init__.py"

with open(file_path, 'r') as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    if line.strip().startswith('"version":'):
        version_info = re.search(r'\((\d+), (\d+), (\d+)\)', line)
        if version_info:
            major, minor, subminor = map(int, version_info.groups())
            subminor += 1  # Increment the subminor version
            new_version = f'    "version": ({major}, {minor}, {subminor}),\n'
            lines[i] = new_version
            break

with open(file_path, 'w') as file:
    file.writelines(lines)
