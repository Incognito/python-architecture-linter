from pathlib import Path
from typing import Iterable, Tuple, Union

import astroid

from python_architecture_linter.domain_objects.file import File


def project_to_files(project_path) -> Iterable[File]:
    paths = Path(project_path).glob("**/*.py")
    yield from [File(path) for path in paths]


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
