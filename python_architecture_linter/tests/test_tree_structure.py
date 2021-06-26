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

    assert results == []
