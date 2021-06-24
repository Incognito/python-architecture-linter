import astroid

from python_architecture_linter.tree_structure.structure import Structure

from python_architecture_linter.linter import lint

from python_architecture_linter.read_file import File, ProjectFileScanner


def test_structure():
    def project_must(target): 
        return target

    def file_must(target): 
        return target.get_path().name

    def provider_ast_must(target): 
        return target.as_string()

    def project_to_files(project_path):
        yield from ProjectFileScanner().get_files_in_project(project_path)

    def file_to_provider_ast(file):
        if file.get_path().name == "provider.py":
            string_file = file.get_contents()
            yield astroid.parse(
                string_file,
                path=file.get_path().absolute()
            )


    sut_provider_ast=Structure('PROVIDER_AST', {})
    sut_provider_ast.must([provider_ast_must])

    sut_file= Structure('FILE', {
        'PROVIDER_AST': file_to_provider_ast
    })
    sut_file.must([file_must])
    sut_file.has([sut_provider_ast])

    sut_project = Structure('PROJECT', {
        'FILE': project_to_files
    })
    sut_project.must([project_must])
    sut_project.has([sut_file])

    path='/home/brian/python-architecture-linter/python_architecture_linter/tests/cases/modular_provider_architecture'  # noqa: E501

    results = list(lint(sut_project, path))

    assert results == [
        '/home/brian/python-architecture-linter/python_architecture_linter/tests/cases/modular_provider_architecture',
        '__init__.py',
        'logic.py',
        'provider.py',
        'from modular_provider_architecture.logic_module.logic import Logic\n\n\nclass LogicProvider:\n    \n    def provide_logic_one(self) -> Logic:\n        return self._create_logic(1)\n    \n    def provide_logic_two(self) -> Logic:\n        return self._create_logic(2)\n    \n    def _create_logic(self, variation) -> Logic:\n        return Logic(variation)\n\n\n',
        '__init__.py',
        'runtime.py',
        'provider.py',
        'from functools import cache\nfrom modular_provider_architecture.logic_module.logic import Logic\nfrom modular_provider_architecture.logic_module.provider import LogicProvider\nfrom .runtime import Runtime\n\n\nclass RuntimeProvider:\n    \n    def provide_runtime(self) -> Runtime:\n        logic_one = self._provide_logic_one()\n        logic_two = self._provide_logic_two()\n        return Runtime([logic_one, logic_two])\n    \n    def _provide_logic_one(self) -> Logic:\n        return self._provide_logic_provider().provide_logic_one()\n    \n    def _provide_logic_two(self) -> Logic:\n        return self._provide_logic_provider().provide_logic_two()\n    \n    @cache\n    def _provide_logic_provider(self) -> LogicProvider:\n        return LogicProvider()\n\n\n',
        'run.py',
        '__init__.py'
    ]

