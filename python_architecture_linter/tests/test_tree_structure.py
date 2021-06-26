import astroid

from python_architecture_linter.linter import lint
from python_architecture_linter.tree_structure import Structure


def test_structure():
    # todo fix test
    sut_branch = Structure("BRANCH")
    sut_branch.must([])

    sut_root = Structure("ROOT")
    sut_root.must([project_must])
    sut_root.has([sut_file])

    path = "/home/brian/python-architecture-linter/python_architecture_linter/tests/cases/modular_provider_architecture"  # noqa: E501

    results = sut_project

    assert results == []
