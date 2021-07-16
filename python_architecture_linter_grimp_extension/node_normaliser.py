from dataclasses import dataclass
from typing import Iterable

import astroid


@dataclass(frozen=True)
class ImportDTO:
    importer: str
    imported: str
    line_number: int
    line_contents: str


def normalise_import_from(import_statement: astroid.nodes.ImportFrom) -> Iterable[ImportDTO]:
    module = import_statement.root()

    imported = module.relative_to_absolute_name(import_statement.modname, import_statement.level)

    yield ImportDTO(
        importer=module.name,
        imported=imported,
        line_number=import_statement.lineno,
        line_contents=import_statement.as_string(),
    )


def normalise_import(import_statement: astroid.nodes.Import) -> Iterable[ImportDTO]:
    importer_module = import_statement.root().name

    for name in import_statement.names:
        yield ImportDTO(
            importer=importer_module,
            imported=import_statement.modname,
            line_number=import_statement.lineno,
            line_contents=import_statement.as_string(),
        )
