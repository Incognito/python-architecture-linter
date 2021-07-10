from pathlib import Path
from typing import Callable, Iterable, List, Tuple, Union

import astroid

from python_architecture_linter.domain_objects.file import File


# todo find better names, to_files and to_file is easy to conflate
def project_to_files(project_path: str) -> Iterable[List[File]]:
    """
    When you want all files at the same time
    """
    paths = Path(project_path).glob("**/*")
    yield [File(path) for path in paths if path.is_file()]


def project_to_file(project_path: str) -> Iterable[File]:
    """
    When you want files one-by-one
    """
    paths = Path(project_path).glob("**/*")
    yield from (File(path) for path in paths if path.is_file())


def project_to_file_filtered(file_filter: Callable[[Path], bool], project_path: str) -> Iterable[File]:
    """
    When you want files one-by-one
    """
    paths = Path(project_path).glob("**/*")
    yield from (File(path) for path in paths if file_filter(path) and path.is_file())


def file_to_ast(file: File) -> Iterable[astroid.node_classes.NodeNG]:
    string_file = file.get_contents()
    file_path = file.get_path().absolute()
    yield astroid.parse(string_file, path=file_path)


def ast_node_to_specific_children(
    child_types: Union[astroid.node_classes.NodeNG, Tuple[astroid.node_classes.NodeNG]],
    node: astroid.node_classes.NodeNG,
) -> Iterable[astroid.node_classes.NodeNG]:
    child_nodes = node.get_children()
    yield from (child_node for child_node in child_nodes if isinstance(child_node, child_types))
