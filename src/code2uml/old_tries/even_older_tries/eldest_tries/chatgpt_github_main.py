"""main code file"""
import os
import subprocess

import pygit2


# Replace with the path to your repository
repo_path = 'examples/repo_example1'

# Create a Git repository object
repo = pygit2.Repository(repo_path)

# Create a list to store UML diagram definitions
uml_diagrams = []

# Iterate through each commit in the repository
for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL | pygit2.GIT_SORT_REVERSE):
    # Get the commit message and author information
    commit_message = commit.message.strip()
    author_name = commit.author.name
    author_email = commit.author.email

    # Get the diff for the commit
    diff = commit.tree.diff_to_tree()

    # Iterate through each file in the commit's diff
    for patch in diff:
        file_path = patch.delta.new_file.path
        file_extension = os.path.splitext(file_path)[1]

        # Check if the file is a supported source code file (e.g., .py, .java, .cpp)
        if file_extension in ['.py', '.java', '.cpp']:
            # Get the content of the file at this commit
            file_blob = repo.get(patch.delta.new_file.id)

            # Create a PlantUML class diagram entry for the file
            class_diagram_entry = f'[{author_name}] -> [{file_path}] : {commit_message}\n'

            # Append the class diagram entry to the list
            uml_diagrams.append(class_diagram_entry)

# Generate the PlantUML diagram content
uml_content = "@startuml\n"
uml_content += "skinparam monochrome true\n"
uml_content += "\n".join(uml_diagrams)
uml_content += "@enduml\n"

print(uml_content)

# Write the PlantUML content to a file
with open('uml_diagram.puml', 'w') as uml_file:
    uml_file.write(uml_content)
    


# # Convert PlantUML file to an image (requires PlantUML executable)
# subprocess.call(['plantuml', 'uml_diagram.puml'])