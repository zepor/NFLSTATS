import os
from generateDS import generateDS

# Directory path containing .xsd files
directory = '/home/zepor/ssweb/backend-container/src/models/'

# Get a list of all .xsd files in the directory
xsd_files = [file for file in os.listdir(directory) if file.endswith('.xsd')]

# Generate schema based on each .xsd file
for xsd_file in xsd_files:
    xsd_path = os.path.join(directory, xsd_file)
    generateDS(xsd_path)
