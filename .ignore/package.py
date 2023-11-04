import pkg_resources
import re

# Path to the vulture output file
file_path = 'vulture_output.txt'

# Extract unused imports from vulture's output
unused_imports = set()
with open(file_path, 'r') as file:
    for line in file:
        # Simple way: just check if "unused import" is in the line
        if 'unused import' in line:
            # Extract the module name using regex (this assumes the module name doesn't contain spaces)
            match = re.search(r'unused import: (\S+)', line)
            if match:
                unused_imports.add(match.group(1))

# Get a list of all installed packages
installed_packages = {d.key for d in pkg_resources.working_set}

unused_packages = set()

for unused_import in unused_imports:
    if unused_import in installed_packages:
        unused_packages.add(unused_import)

print("Potentially unused packages:", unused_packages)

