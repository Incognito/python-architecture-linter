from dataclasses import dataclass
from typing import Iterator

from grimp.adaptors.graph import ImportGraph


@dataclass
class PackageMetrics:
    package_name: str
    afferent_coupling: int
    efferent_coupling: int
    instability: float


def compute_metrics(graph: ImportGraph, module: str) -> PackageMetrics:
    """
    Afferent Coupling
        - How many modules a target package imports
        - Generic/Abstract packages should have few to avoid making them change
          often as their changes will likely "cascade" into many other parts of
          software causing a lot of additional refactoring when updating code.

    Efferent Coupling
        - How many other packages import a target package
        - Ideally "more concrete" packages will import instead of "more
          abstract" packages, this keeps frequently-changing details to the
          ends of dependency chains where changes will not "cascade" into
          multiple places.

                         ┌───┐    ┌───┐
             Afferent ───►1.0├────►0.0────► Efferent
                         └───┘    └───┘
    Instability
        - Ratio indicating how resilient or fragile a package is when changed.
        - 0 is resilient, 1 is fragile.
        - 0 means nobody is importing the module, 1 means it is heavily imported
          and is correlated with cascading refactors over many parts of the code
        - Instable packages should be heavily concrete, stable packages should
          be more abstract
        - Instable packages should depend on more stable ones to avoid "cascading
          changes".

             = efferent / (efferent + afferent)

    Abstractness (not implemented)
        - Determine if a package is mostly abstract code or not (for example,
          interfaces).
        - Hard to do in Python, so it isn't implemented. If you have a good way
          to do it, please reach out with a pull request so we can try to add
          it.

    Distance From Main Sequence (not implemented)
        - "Main Sequence" is an approximated ratio of abstractness vs instability.
        - Do not confuse "main sequence" with the sequence of dependencies in a
          dependency graph itself, in this case sequence just means ratio
          between abstract and instable. It has nothing to do with the shape of
          the graph.
        - It can warn you if a package is overly abstract or under-abstracted
          based on how it is used.
        - If you have a lot of distance, it likely means you must refactor by
          creating two packages.
    """

    afferent_coupling = len(graph.find_modules_directly_imported_by(module))
    efferent_coupling = len(graph.find_modules_that_directly_import(module))
    instability = efferent_coupling / (efferent_coupling + afferent_coupling)

    return PackageMetrics(
        package_name=module,
        afferent_coupling=afferent_coupling,
        efferent_coupling=efferent_coupling,
        instability=instability,
    )


def get_all_package_metrics(graph: ImportGraph) -> Iterator[PackageMetrics]:
    for module in graph.modules:
        yield compute_metrics(graph, module)
