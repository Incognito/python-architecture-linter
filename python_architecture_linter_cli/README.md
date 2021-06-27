A basic CLI wrapper for the python architecture linter using click


# Public API:

This function is public API, a breaking chance will force a major release:

```
def lint_command_factory(project_definition: Structure) -> click.Command:
```

# Anticipated usage

```
from modular_provider_architecture_definition import project_definition
from python_architecture_linter_cli import lint_command

lint_command = lint_command_factory(project_definition)
if __name__ == '__main__':
    lint_command()
```


# Project

The project is maintained in a monorepo at https://github.com/Incognito/python-architecture-linter
