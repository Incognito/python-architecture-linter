from pathlib import Path
from typing import Callable, Iterable, List, Tuple, Union

import astroid

from python_architecture_linter.domain_objects.file import File
from python_architecture_linter.file_to_module import file_to_module


# todo find better names, to_files and to_file is easy to conflate
def project_to_files(project_path: str) -> Iterable[List[File]]:
    """
    When you want all files at the same time
    """
    project_root = Path(project_path)
    paths = project_root.glob("**/*")
    yield [File(path=path, project_root=project_root) for path in paths if path.is_file()]


def project_to_file(project_path: str) -> Iterable[File]:
    """
    When you want files one-by-one
    """
    project_root = Path(project_path)
    paths = project_root.glob("**/*")
    yield from (File(path=path, project_root=project_root) for path in paths if path.is_file())


def project_to_file_filtered(file_filter: Callable[[Path], bool], project_path: str) -> Iterable[File]:
    """
    When you want files one-by-one but filtered
    """
    project_root = Path(project_path)
    paths = project_root.glob("**/*")
    yield from (File(path=path, project_root=project_root) for path in paths if file_filter(path) and path.is_file())


def file_to_ast(file: File) -> Iterable[astroid.node_classes.NodeNG]:
    string_file = file.get_contents()
    file_path = file.get_path().absolute().as_posix()
    project_root = file.get_project_root().absolute().as_posix()
    module_name = file_to_module(project_root, file_path)

    module = astroid.parse(string_file, path=file_path, module_name=module_name)

    yield module


def ast_node_to_specific_children(
    child_types: Union[astroid.node_classes.NodeNG, Tuple[astroid.node_classes.NodeNG]],
    node: astroid.node_classes.NodeNG,
) -> Iterable[astroid.node_classes.NodeNG]:
    child_nodes = node.get_children()
    yield from (child_node for child_node in child_nodes if isinstance(child_node, child_types))
