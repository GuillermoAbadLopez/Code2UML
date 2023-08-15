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
        file_extension = os.path.splitext(file_name)[1]
        
        # To avoid duplicated classes from the __inits__
        # Check if the file is a supported source code file (e.g., .py, .java, .cpp)
        if file_name != "__init__.py" and file_extension in ['.py', '.java', '.cpp']:
            file_path = os.path.join(root, file_name)

            # Get the directory containing the file
            module_dir = os.path.dirname(file_path)

            # Add the module directory temporarily to sys.path
            sys.path.insert(0, module_dir)

            try:
                # Import the module to inspect its contents
                module_name = os.path.splitext(os.path.basename(file_name))[0]
                module = __import__(module_name)

                # Get class information from the module
                classes = [cls_name for cls_name, cls_obj in inspect.getmembers(module) if inspect.isclass(cls_obj)]

                # Create a PlantUML class diagram entry for each class
                for cls_name in classes:
                    class_diagram_entry = f'[{cls_name}] -down-|> [{file_path}]\n'
                    uml_diagrams.append(class_diagram_entry)

            finally:
                # Remove the temporarily added module directory from sys.path
                sys.path.pop(0)

# Generate the PlantUML diagram content
uml_content = "@startuml\n"
uml_content += "skinparam monochrome true\n"
uml_content += "\n".join(uml_diagrams)
uml_content += "@enduml\n"

# Write the PlantUML content to a file
with open('uml_diagram_with_imports.puml', 'w') as uml_file:
    uml_file.write(uml_content)

# # Convert PlantUML file to an image (requires PlantUML executable)
# subprocess.call(['plantuml', 'uml_diagram.puml'])