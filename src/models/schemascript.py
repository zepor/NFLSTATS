import glob

files = glob.glob('*.py')  # Adjust the path and file extension as needed
print(files)  # Add this line after the glob.glob call to see what files are found
with open('combined_schema.py', 'w') as outfile:
    for file in files:
        with open(file) as infile:
            outfile.write(infile.read())
        outfile.write("\n\n")  # Add line breaks between files
       
