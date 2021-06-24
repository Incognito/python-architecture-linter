import astroid

from python_architecture_linter.lint_provider_class import provider_class_linter
from python_architecture_linter.read_file import File, ProjectFileScanner

from python_architecture_linter.ast_validators.module_validators import validate_provider_module_contents


class FileParser:
    def to_ast(self, file: File):
        string_file = file.get_contents()
        return astroid.parse(string_file, path=file.get_path().absolute())


def validate_provider(file: File):
    ast_provider_file = FileParser().to_ast(file)
    return provider_class_linter.lint(ast_provider_file)


def lint(path):
    files = ProjectFileScanner().get_files_in_project(path)

    # rule: modules with providers should be on the root level of a module
    # rule: provider must not be in files other than provider.py
    # rule: instances only created in provider (except for DTOs)
    # rule: runtime modules have a run.py

    provider_files = filter(lambda file: file.get_path().name == "provider.py", files)
    results = []
    for provider_file in provider_files:
        # rule: provider may be in module/provider.py
        validated_results = validate_provider(provider_file)
        results = [*results, *validated_results]

    return results
