import xmlschema
import os


def parse_xsd(directory_path):
    xsd_schemas = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.xsd'):
            file_path = os.path.join(directory_path, filename)
            xsd_schemas[filename] = xmlschema.XMLSchema(file_path)
    return xsd_schemas


# Replace with the directory where your XSD files are stored
xsd_directory = '.'
xsd_schemas = parse_xsd(xsd_directory)
