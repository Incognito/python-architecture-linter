import os
from pathlib import Path

import astroid

from python_architecture_linter.domain_objects.file import File
from python_architecture_linter.node_navigators import (
    ast_node_to_specific_children,
    file_to_ast,
    project_to_file,
    project_to_file_filtered,
    project_to_files,
)


def test_project_to_files():
    # Arrange
    # Act
    sut = list(project_to_files(os.path.dirname(os.path.realpath(__file__)) + "/fixtures"))

    # Assert
    assert len(sut) == 1
    assert len(sut[0]) == 4


def test_project_to_file():
    # Arrange
    # Act
    sut = list(project_to_file(os.path.dirname(os.path.realpath(__file__)) + "/fixtures"))

    # Assert
    assert len(sut) == 4


def test_project_to_file_filtered():
    # Arrange
    def filter_func(path: Path) -> bool:
        return "3" in path.name

    # Act

    sut = list(project_to_file_filtered(filter_func, os.path.dirname(os.path.realpath(__file__)) + "/fixtures"))

    # Assert
    assert len(sut) == 1
    assert "empty_file3" in sut[0].get_path().name


def test_file_to_ast():
    # Arrange
    class MockFile(File):
        def get_contents(self) -> str:
            return """
            print("hello world")
            """

    file = MockFile(Path("fakefile"))

    # Act
    sut = list(file_to_ast(file))

    # Assert
    assert len(sut) == 1
    assert list(sut[0].get_children())[0].value.args[0].value == "hello world"


def test_ast_node_to_specific_children():
    # Arrange
    root_node = astroid.parse(
        """
    foo = 1

    def hello():
        pass

    print("test")
    """
    )

    # Act
    sut = list(ast_node_to_specific_children((astroid.nodes.FunctionDef), root_node))

    # Assert
    assert len(sut) == 1
