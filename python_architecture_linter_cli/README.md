A basic CLI wrapper for the python architecture linter using click


# Key Features

1. Lint entire project architecture based on an injected definition
1. Maintain a list of excuses for architecture violations which permits CI to pass


```
Usage: python-architecture-linter [OPTIONS] [PATH]

  Runs linter and reports results.

Options:
  --show-success BOOLEAN        Show successful validation attempts too
  --with-excuses BOOLEAN        Excuse results stored in excuses.yml
  --excuse-path TEXT            path of excuses.yml
  --write-excuses-file BOOLEAN  Replace the excuse file with all violations
  --help                        Show this message and exit.
```

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
