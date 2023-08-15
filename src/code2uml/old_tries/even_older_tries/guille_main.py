""" main file created by Guille idea"""
import os
import subprocess
import inspect
import sys

# Replace with the path to your local directory containing code files
directory_path = 'examples/repo_example1'

# Create a list to store UML diagram definitions
uml_diagrams = []

# Iterate through each file in the directory
for root, _, files in os.walk(directory_path):
    for file_name in files:
        if file_name != "__init__":
            file_extension = os.path.splitext(file_name)[1]

            # Check if the file is a supported source code file (e.g., .py, .java, .cpp)
            if file_extension in ['.py', '.java', '.cpp']:
                file_path = os.path.join(root, file_name)

                # Get the classes of the file
                classes = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules[file_path]) if inspect.isclass(cls_obj)]

                # Create a PlantUML class diagram entry for the file
                class_diagram_entry = f'[{file_path}] : {classes}\n'

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