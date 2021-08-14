from modular_provider_architecture_definition.definition import project_definition
from python_architecture_linter.node_navigators import project_to_files
from python_architecture_linter_cli import lint_command_factory
from python_architecture_linter_grimp_extension.grimp_definition import project_files

project_definition._navigation["ALL_PATHON_FILES"] = project_to_files
project_definition.has([project_files])
lint_command = lint_command_factory(project_definition)

if __name__ == "__main__":
    lint_command()
