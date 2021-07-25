from grimp.adaptors.graph import ImportGraph
from grimp_package_metrics.dependency_cycles import dependency_cycles


def test_multiple_cycles():
    # Arrange
    graph = ImportGraph()

    # chain imports a->b->c->d-e>->f->g
    graph.add_import(importer="a", imported="b")
    graph.add_import(importer="b", imported="c")
    graph.add_import(importer="c", imported="d")
    graph.add_import(importer="d", imported="e")
    graph.add_import(importer="e", imported="f")
    graph.add_import(importer="f", imported="g")

    # cycle1 g->a
    graph.add_import(importer="g", imported="a")

    # cycle2 d->b
    graph.add_import(importer="d", imported="b")

    # cycle3 x->y->z->x
    graph.add_import(importer="x", imported="y")
    graph.add_import(importer="y", imported="z")
    graph.add_import(importer="z", imported="x")

    # Act
    sut = list(dependency_cycles(graph))

    # Assert

    # Order of cycles can change without warning
    set_results = [set(cycle) for cycle in sut]
    assert len(set_results) == 3
    for result in set_results:
        assert result in [set(["y", "z", "x"]), set(["d", "b", "c"]), set(["d", "e", "f", "g", "a", "b", "c"])]


def test_self_cylcles_are_ignored():
    # Arrange
    graph = ImportGraph()
    graph.add_import(importer="a", imported="a")
    graph.add_import(importer="a", imported="b")

    # Act
    sut = list(dependency_cycles(graph))

    # Assert
    assert sut == []
