import os
import subprocess
import ast

# Replace with the path to your local directory containing code files
directory_path = 'examples/repo_example2'

# Create a dictionary to store class and argument information
class_info_dict = {}

# Function to extract class and constructor argument information from an AST node
def extract_class_and_arguments(node):
    for item in node.body:
        if isinstance(item, ast.ClassDef):
            base_classes = []
            arguments = {}

            for base in item.bases:
                if isinstance(base, ast.Name):
                    base_classes.append(base.id)
                elif isinstance(base, ast.Attribute):
                    base_classes.append(base.attr)

            for stmt in item.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == '__init__':
                    for arg in stmt.args.args:
                        if arg.annotation:
                            arg_type = arg.annotation.id if isinstance(arg.annotation, ast.Name) else 'Any' 
                            if arg_type not in ['Any', 'str', 'int', 'float'] and arg_type not in arguments.values():
                                arguments[arg.arg] = arg_type # arg.arg is the arg_name           
                    if not arguments:
                        arguments[''] = ''

            class_info_dict[item.name] = base_classes, arguments # item.name is the class_name

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
                extract_class_and_arguments(parsed)
            except SyntaxError:
                print(f"Error parsing {file_path}")
                
class_diagrams=''
# Iterate through class and argument information            
for class_name, values in class_info_dict.items():
    base_str = f': {", ".join(values[0])}' if values[0] else ''
    arguments_str = ", ".join([f"{arg_type}" for _, arg_type in values[1].items()]) if values[1] else None
    
    final_arguments_str = f'<- {arguments_str}' if arguments_str else ''
    class_diagrams += f'[{class_name}{base_str}] {final_arguments_str}\n\n'
    
# Generate the PlantUML diagram content
uml_content = "@startuml\n"
uml_content += "skinparam monochrome true\n"
uml_content += class_diagrams
uml_content += "@enduml\n"

# Write the PlantUML content to a file
with open('uml_diagram.puml', 'w') as uml_file:
    uml_file.write(uml_content)

# # Convert PlantUML file to an image (requires PlantUML executable)
# subprocess.call(['plantuml', 'uml_diagram.puml'])