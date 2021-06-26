import os

from modular_provider_architecture_definition.definition import project

from python_architecture_linter.linter import lint


def test_definition():
    path = os.path.dirname(os.path.realpath(__file__)) + "/tests/cases/modular_provider_architecture"  # noqa: E501
    results = list(lint(project, path))
    assert results == []
