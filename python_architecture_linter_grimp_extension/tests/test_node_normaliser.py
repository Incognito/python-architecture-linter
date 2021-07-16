import astroid

from python_architecture_linter_grimp_extension.node_normaliser import (
    ImportDTO,
    normalise_import,
    normalise_import_from,
)


def test_multiple_import():
    # Arrange
    statement = astroid.parse("import foo, bar")
    statement.name = "any.module.path"
    import_statement = statement.body[0]

    # Act
    sut = list(normalise_import(import_statement))

    # Assert
    assert sut == [
        ImportDTO(importer="any.module.path", imported="foo", line_number=1, line_contents="import foo, bar"),
        ImportDTO(importer="any.module.path", imported="bar", line_number=1, line_contents="import foo, bar"),
    ]


def test_import_with_alias():
    # Arrange
    statement = astroid.parse("import foo as foo_alias")
    statement.name = "any.module.path"
    import_statement = statement.body[0]

    # Act
    sut = list(normalise_import(import_statement))

    # Assert
    assert sut == [
        ImportDTO(importer="any.module.path", imported="foo", line_number=1, line_contents="import foo as foo_alias")
    ]


def test_import():
    # Arrange
    statement = astroid.parse("import foo")
    statement.name = "any.module.path"
    import_statement = statement.body[0]

    # Act
    sut = list(normalise_import(import_statement))

    # Assert
    assert sut == [ImportDTO(importer="any.module.path", imported="foo", line_number=1, line_contents="import foo")]


def test_import_from():
    # Arrange
    statement = astroid.parse("from foo import bar")
    statement.name = "any.module.path"
    import_statement = statement.body[0]

    # Act
    sut = list(normalise_import_from(import_statement))

    # Assert
    assert sut == [
        ImportDTO(importer="any.module.path", imported="foo", line_number=1, line_contents="from foo import bar")
    ]


def test_import_from_alias():
    # Arrange
    statement = astroid.parse("from foo import bar as baz")
    statement.name = "any.module.path"
    import_statement = statement.body[0]

    # Act
    sut = list(normalise_import_from(import_statement))

    # Assert
    assert sut == [
        ImportDTO(importer="any.module.path", imported="foo", line_number=1, line_contents="from foo import bar as baz")
    ]


def test_import_from_relative_1_level():
    # Arrange
    statement = astroid.parse("from .foo import bar")
    statement.name = "any.module.path"
    import_statement = statement.body[0]

    # Act
    sut = list(normalise_import_from(import_statement))

    # Assert
    assert sut == [
        ImportDTO(
            importer="any.module.path", imported="any.module.foo", line_number=1, line_contents="from .foo import bar"
        )
    ]


def test_import_from_relative_2_levels():
    # Arrange
    statement = astroid.parse("from ..foo import bar")
    statement.name = "any.module.path"
    import_statement = statement.body[0]

    # Act
    sut = list(normalise_import_from(import_statement))

    # Assert
    assert sut == [
        ImportDTO(importer="any.module.path", imported="any.foo", line_number=1, line_contents="from ..foo import bar")
    ]
