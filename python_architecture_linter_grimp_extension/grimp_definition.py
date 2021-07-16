from python_architecture_linter import Structure
from python_architecture_linter.node_navigators import project_to_files
from python_architecture_linter_grimp_extension.grimp_navigators import (
    files_to_import_statements,
    import_statements_to_graph,
)

def must(graph):
    print(graph.modules)

import_graph = Structure("IMPORT_GRAPH", {})
import_graph.must([must])


import_statements = Structure("IMPORT_STATEMENTS", {"IMPORT_GRAPH": import_statements_to_graph})
import_statements.has([import_graph])


project_files = Structure("ALL_PATHON_FILES", {"IMPORT_STATEMENTS": files_to_import_statements})
project_files.has([import_statements])


project = Structure("PROJECT", {"ALL_PATHON_FILES": project_to_files})
project.has([project_files])
