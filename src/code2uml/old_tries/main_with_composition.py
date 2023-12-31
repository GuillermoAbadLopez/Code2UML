import os
import subprocess
import ast

# Replace with the path to your local directory containing code files
directory_path = 'examples/repo_example1'

# Create a dictionary to store class and argument information
class_info_dict = {}

# Function to extract class and constructor argument information from an AST node
def extract_class_and_arguments(node):
    for item in node.body:
        if isinstance(item, ast.ClassDef):
            class_name = item.name
            arguments = {}

            for stmt in item.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == '__init__':
                    for arg in stmt.args.args:
                        arg_name = arg.arg
                        if arg.annotation:
                            arg_type = arg.annotation.id if isinstance(arg.annotation, ast.Name) else 'Any'
                            arguments[arg_name] = arg_type
                        else:
                            arguments[arg_name] = 'Any'  # Default type if no annotation

            class_info_dict[class_name] = arguments

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
                extract_class_and_arguments(parsed)
            except SyntaxError:
                print(f"Error parsing {file_path}")

# Generate the PlantUML diagram content
uml_content = "@startuml\n"
uml_content += "skinparam monochrome true\n"

# Iterate through class and argument information
for class_name, arguments in class_info_dict.items():
    if arguments:
        arguments_str = ', '.join([f"{arg}: {arg_type}" for arg, arg_type in arguments.items()])
        class_diagram_entry = f'[{class_name}] : {arguments_str}\n\n'
        uml_content += class_diagram_entry

uml_content += "@enduml\n"

# Write the PlantUML content to a file
with open('uml_diagram_with_composition.puml', 'w') as uml_file:
    uml_file.write(uml_content)

# # Convert PlantUML file to an image (requires PlantUML executable)
# subprocess.call(['plantuml', 'uml_diagram.puml'])