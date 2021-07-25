from grimp.adaptors.graph import ImportGraph
from grimp_package_metrics.coupling_metrics import (
    PackageMetrics,
    get_all_package_metrics,
)


def test_metrics():
    # Arrange
    graph = ImportGraph()
    # chain imports a->b->c->d
    graph.add_import(importer="a", imported="b")
    graph.add_import(importer="b", imported="c")
    graph.add_import(importer="c", imported="d")

    # An extra dependency on c
    graph.add_import(importer="d", imported="c")

    # Everything depends on z
    graph.add_import(importer="a", imported="z")
    graph.add_import(importer="b", imported="z")
    graph.add_import(importer="c", imported="z")
    graph.add_import(importer="d", imported="z")

    # Act
    sut = list(get_all_package_metrics(graph))
    sorted_sut = sorted(sut, key=lambda package_metrics: package_metrics.package_name)

    # Assert
    assert sorted_sut == [
        PackageMetrics(package_name="a", afferent_coupling=2, efferent_coupling=0, instability=0.0),
        PackageMetrics(package_name="b", afferent_coupling=2, efferent_coupling=1, instability=0.3333333333333333),
        PackageMetrics(package_name="c", afferent_coupling=2, efferent_coupling=2, instability=0.5),
        PackageMetrics(package_name="d", afferent_coupling=2, efferent_coupling=1, instability=0.3333333333333333),
        PackageMetrics(package_name="z", afferent_coupling=0, efferent_coupling=4, instability=1.0),
    ]
