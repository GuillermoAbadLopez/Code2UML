import os
import subprocess
import ast

# Replace with the path to your local directory containing code files
directory_path = 'examples/repo_example1'

# Create a list to store UML diagram definitions
uml_diagrams = []

# Function to extract class names from an AST node
def extract_classes(node):
    classes = []
    for item in node.body:
        if isinstance(item, ast.ClassDef):
            classes.append(item.name)
    return classes

# Iterate through each file in the directory
for root, _, files in os.walk(directory_path):
    for file_name in files:
        file_extension = os.path.splitext(file_name)[1]

        # Check if the file is a supported source code file (e.g., .py, .java, .cpp)
        if file_extension == '.py':
            file_path = os.path.join(root, file_name)

            with open(file_path, 'r') as file:
                code = file.read()

            # Parse the code using AST
            try:
                parsed = ast.parse(code)
                classes = extract_classes(parsed)
                for cls_name in classes:
                    class_diagram_entry = f'[{cls_name}] -down-|> [{file_path}]\n'
                    uml_diagrams.append(class_diagram_entry)
            except SyntaxError:
                print(f"Error parsing {file_path}")

# Generate the PlantUML diagram content
uml_content = "@startuml\n"
uml_content += "skinparam monochrome true\n"
uml_content += "\n".join(uml_diagrams)
uml_content += "@enduml\n"

# Write the PlantUML content to a file
with open('uml_diagram_without_imports.puml', 'w') as uml_file:
    uml_file.write(uml_content)

# # Convert PlantUML file to an image (requires PlantUML executable)
# subprocess.call(['plantuml', 'uml_diagram.puml'])