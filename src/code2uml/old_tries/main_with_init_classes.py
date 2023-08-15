import os
import subprocess
import ast

# Replace with the path to your local directory containing code files
directory_path = 'examples/repo_example1'

# Create a list to store UML diagram definitions
uml_diagrams = []

# Function to extract classes used in __init__ methods from an AST node
def extract_init_classes(node):
    init_classes = set()

    class InitVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            if node.name == "__init__":
                for stmt in node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                        if isinstance(stmt.value.func, ast.Name):
                            init_classes.add(stmt.value.func.id)
                        elif isinstance(stmt.value.func, ast.Attribute):
                            init_classes.add(stmt.value.func.attr)
            self.generic_visit(node)

    visitor = InitVisitor()
    visitor.visit(node)
    return init_classes

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
                init_classes = extract_init_classes(parsed)
                for cls_name in init_classes:
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
with open('uml_diagram_with_init_classes.puml', 'w') as uml_file:
    uml_file.write(uml_content)

# # Convert PlantUML file to an image (requires PlantUML executable)
# subprocess.call(['plantuml', 'uml_diagram.puml'])