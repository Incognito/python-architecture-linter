from typing import Iterator, List

import networkx
from grimp.adaptors.graph import ImportGraph


def dependency_cycles(graph: ImportGraph) -> Iterator[List[str]]:
    # Violates private internals of grimp by accessing private implementation
    cycles = networkx.simple_cycles(graph._networkx_graph)

    for cycle in cycles:
        if len(cycle) > 1:
            yield cycle
