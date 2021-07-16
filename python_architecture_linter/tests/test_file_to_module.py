import pytest

from python_architecture_linter.file_to_module import file_to_module


@pytest.mark.xfail(reason="Logic to deal with this case is not implemented")
def test_directory_path_is_handled():
    # Arrange
    project_path = "/foo-project"
    target_file = "/foo-project/foo_project"

    # Act
    sut = file_to_module(project_path, target_file)

    # Assert
    expected = "it should probably throw an exception"
    assert sut == expected


@pytest.mark.xfail(reason="Logic to deal with this case is not implemented")
def test_file_outside_of_project_is_handled():
    # Arrange
    project_path = "/foo-project/foo_project"
    target_file = "/bar-project/bar_project/target.py"

    # Act
    sut = file_to_module(project_path, target_file)

    # Assert
    expected = "it should probably throw an exception"
    assert sut == expected


def test_file_in_project_root_provides_correct_path_and_tailing_directory_seperator():
    # Arrange
    project_path = "/foo-project/"
    target_file = "/foo-project/foo_project/target.py"

    # Act
    sut = file_to_module(project_path, target_file)

    # Assert
    expected = "foo_project.target"
    assert sut == expected


def test_file_in_project_root_provides_correct_path():
    # Arrange
    project_path = "/foo-project"
    target_file = "/foo-project/foo_project/target.py"

    # Act
    sut = file_to_module(project_path, target_file)

    # Assert
    expected = "foo_project.target"
    assert sut == expected


def test_init_file_in_project_root_provides_correct_path():
    # Arrange
    project_path = "/foo-project"
    target_file = "/foo-project/foo_project/__init__.py"

    # Act
    sut = file_to_module(project_path, target_file)

    # Assert
    expected = "foo_project"
    assert sut == expected


def test_init_file_in_project_folder_provides_correct_path():
    # Arrange
    project_path = "/foo-project"
    target_file = "/foo-project/foo_project/sub_folder/__init__.py"

    # Act
    sut = file_to_module(project_path, target_file)

    # Assert
    expected = "foo_project.sub_folder"
    assert sut == expected


def test_file_in_project_folder_provides_correct_path():
    # Arrange
    project_path = "/foo-project"
    target_file = "/foo-project/foo_project/sub_folder/target.py"

    # Act
    sut = file_to_module(project_path, target_file)

    # Assert
    expected = "foo_project.sub_folder.target"
    assert sut == expected
