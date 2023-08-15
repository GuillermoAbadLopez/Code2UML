import os
import subprocess
import ast

# Replace with the path to your local directory containing code files
directory_path = 'examples/repo_example1'

# Create a list to store UML diagram definitions
uml_diagrams = []

# Function to extract class names and inheritance information from an AST node
def extract_classes_and_inheritance(node):
    classes = {}
    for item in node.body:
        if isinstance(item, ast.ClassDef):
            class_name = item.name
            base_classes = []
            for base in item.bases:
                if isinstance(base, ast.Name):
                    base_classes.append(base.id)
                elif isinstance(base, ast.Attribute):
                    base_classes.append(base.attr)
            classes[class_name] = base_classes
    return classes

# Iterate through each file in the directory
for root, _, files in os.walk(directory_path):
    for file_name in files:
        file_extension = os.path.splitext(file_name)[1]

        # Check if the file is a supported source code file (e.g., .py, .java, .cpp)
        if file_name != "__init__.py" and file_extension == '.py':
            file_path = os.path.join(root, file_name)

            with open(file_path, 'r') as file:
                code = file.read()

            # Parse the code using AST
            try:
                parsed = ast.parse(code)
                classes_info = extract_classes_and_inheritance(parsed)
                for cls_name, base_classes in classes_info.items():
                    if base_classes:
                        base_str = f': {" ".join(base_classes)}'
                    else:
                        base_str = ''
                    class_diagram_entry = f'[{cls_name}{base_str}] -down-|> [{file_path}]\n'
                    uml_diagrams.append(class_diagram_entry)
            except SyntaxError:
                print(f"Error parsing {file_path}")

# Generate the PlantUML diagram content
uml_content = "@startuml\n"
uml_content += "skinparam monochrome true\n"
uml_content += "\n".join(uml_diagrams)
uml_content += "@enduml\n"

# Write the PlantUML content to a file
with open('uml_diagram_with_inheritance.puml', 'w') as uml_file:
    uml_file.write(uml_content)

# # Convert PlantUML file to an image (requires PlantUML executable)
# subprocess.call(['plantuml', 'uml_diagram.puml'])