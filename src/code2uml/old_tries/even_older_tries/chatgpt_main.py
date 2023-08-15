import os
import subprocess

# Replace with the path to your local directory containing code files
directory_path = 'examples/repo_example1'

# Create a list to store UML diagram definitions
uml_diagrams = []

# Iterate through each file in the directory
for root, _, files in os.walk(directory_path):
    for file_name in files:
        file_extension = os.path.splitext(file_name)[1]

        # Check if the file is a supported source code file (e.g., .py, .java, .cpp)
        if file_extension in ['.py', '.java', '.cpp']:
            file_path = os.path.join(root, file_name)

            # Create a PlantUML class diagram entry for the file
            class_diagram_entry = f'[{file_path}] : {root}\n'

            # Append the class diagram entry to the list
            uml_diagrams.append(class_diagram_entry)

# Generate the PlantUML diagram content
uml_content = "@startuml\n"
uml_content += "skinparam monochrome true\n"
uml_content += "\n".join(uml_diagrams)
uml_content += "@enduml\n"

# Write the PlantUML content to a file
with open('uml_diagram.puml', 'w') as uml_file:
    uml_file.write(uml_content)
    
print(uml_content)
    


# # Convert PlantUML file to an image (requires PlantUML executable)
# subprocess.call(['plantuml', 'uml_diagram.puml'])