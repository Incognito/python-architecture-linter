from python_architecture_linter.project_linter import lint


def test_method_violations():
    path = "/home/brian/python-architecture-linter/python_architecture_linter/tests/cases/modular_provider_architecture"

    results = lint(path)

    assert results is None
