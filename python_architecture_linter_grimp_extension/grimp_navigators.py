import itertools
from functools import partial
from typing import Iterable, List

import astroid
from grimp.adaptors.graph import ImportGraph

from python_architecture_linter.node_navigators import (
    ast_node_to_specific_children,
    file_to_ast,
)
from python_architecture_linter_grimp_extension.node_normaliser import (
    ImportDTO,
    normalise_import,
    normalise_import_from,
)


def files_to_import_statements(files) -> Iterable:
    python_files = [file for file in files if ".py" in file.get_path().name]

    asts = itertools.chain.from_iterable((file_to_ast(file) for file in python_files))

    import_reducer = partial(ast_node_to_specific_children, (astroid.nodes.Import, astroid.nodes.ImportFrom))

    imports = itertools.chain.from_iterable(
        (import_reducer(ast) for ast in asts)
    )  # fixme, should crawl entire file, not just module body

    normalised_imports = import_statements_to_normalised_import_statements(imports)

    yield normalised_imports


def import_statements_to_normalised_import_statements(import_statements) -> Iterable:
    for import_statement in import_statements:
        if isinstance(import_statement, astroid.nodes.ImportFrom):
            yield from normalise_import_from(import_statement)

        if isinstance(import_statement, astroid.nodes.Import):
            yield from normalise_import(import_statement)


def import_statements_to_graph(imports: List[ImportDTO]) -> Iterable[ImportGraph]:
    graph = ImportGraph()

    for import_dto in imports:
        graph.add_import(
            importer=import_dto.importer,
            imported=import_dto.imported,
            line_number=import_dto.line_number,
            line_contents=import_dto.line_contents,
        )

    yield graph
