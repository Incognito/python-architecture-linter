from modular_provider_architecture_definition.definition import project_definition
from python_architecture_linter_cli import lint_command_factory

lint_command = lint_command_factory(project_definition)
if __name__ == "__main__":
    lint_command()
