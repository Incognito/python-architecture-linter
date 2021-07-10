import itertools
from python_architecture_linter import Structure, Linter

from functools import partial
import astroid

from python_architecture_linter.node_navigators import (
    project_to_files,
    file_to_ast,
    ast_node_to_specific_children
)

import grimp

def _module_name_from_filename(
    filename_and_path: str, package_directory: str
) -> str:
    """
    Args:
        filename_and_path (string) - the full name of the Python file.
        package_directory (string) - the full path of the top level Python package directory.
     Returns:
        Absolute module name for importing (string).
    """

    import os
    def split(file_name: str):
        return os.path.split(file_name)

    container_directory, package_name = split(package_directory)
    internal_filename_and_path = filename_and_path[len(package_directory) :]
    internal_filename_and_path_without_extension = internal_filename_and_path[1:-3]

    components = [
        package_name
    ] + internal_filename_and_path_without_extension.split(os.sep)
    if components[-1] == "__init__":
        pass
        #components.pop() # todo imported needs to know about imported init and relative import level, wow that's messy.
    return ".".join(components)

target_folder = "/home/brian/python-architecture-linter-monorepo/modular_provider_architecture_definition/tests/cases/modular_provider_architecture/modular_provider_architecture"


# print statements build the correct dependency model for this project
#
#   digraph {
#       subgraph module_runtime {
#   "module_runtime.provider" -> "logic_module.logic"
#   "module_runtime.provider" -> "logic_module.provider"
#   "module_runtime.provider" -> "module_runtime.runtime.Runtime"
#   "module_runtime.provider" -> "module_runtime.runtime"
#   "module_runtime.run" -> "module_runtime.provider"
#           label = "module_runtime";
#       }
#       subgraph logic_module {
#   "logic_module.provider" -> "logic_module.logic"
#           label = "logic_module";
#       }
#       "module_runtime.provider" -> "functools"
#   }
#
#                     ┌−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−┐
#                     ╎                             module_runtime                                    ╎
#                     ╎                                                                               ╎
#                     ╎ ┌───────────────────────┐                  ┌────────────────────────────────┐ ╎
#                     ╎ │  module_runtime.run   │                  │ module_runtime.runtime.Runtime │ ╎
#                     ╎ └───────────────────────┘                  └────────────────────────────────┘ ╎
#                     ╎   │                                          ▲                                ╎
#                     ╎   │                                          │                                ╎
#                     ╎   │                                          │                                ╎
#                     ╎   │                                          │                                 −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−┐
#                     ╎   ▼                                          │                                                                 ╎
#   ┌───────────┐     ╎ ┌───────────────────────────────────────────────────────────────────────────┐       ┌────────────────────────┐ ╎
#   │ functools │ ◀── ╎ │                          module_runtime.provider                          │ ────▶ │ module_runtime.runtime │ ╎
#   └───────────┘     ╎ └───────────────────────────────────────────────────────────────────────────┘       └────────────────────────┘ ╎
#                     ╎                                                                                                                ╎
#                     └−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−┘
#                         │                          │
#                         │                          │
#                         ▼                          │
#                     ┌−−−−−−−−−−−−−−−−−−−−−−−−−−−┐  │
#                     ╎       logic_module        ╎  │
#                     ╎                           ╎  │
#                     ╎ ┌───────────────────────┐ ╎  │
#                     ╎ │ logic_module.provider │ ╎  │
#                     ╎ └───────────────────────┘ ╎  │
#                     ╎   │                       ╎  │
#                     ╎   │                       ╎  │
#                     ╎   ▼                       ╎  │
#                     ╎ ┌───────────────────────┐ ╎  │
#                     ╎ │  logic_module.logic   │ ╎ ◀┘
#                     ╎ └───────────────────────┘ ╎
#                     ╎                           ╎
#                     └−−−−−−−−−−−−−−−−−−−−−−−−−−−┘

def files_to_import_graph(files):
    python_files = [file for file in files if ".py" in file.get_path().name]

    asts = itertools.chain.from_iterable((file_to_ast(file) for file in python_files))

    import_reducer = partial(ast_node_to_specific_children, (astroid.nodes.Import, astroid.nodes.ImportFrom))

    imports = itertools.chain.from_iterable((import_reducer(ast) for ast in asts)) # fixme, should crawl entire file, not just module body
    yield list(imports)

def import_statements_to_graph(import_statements):
    module_paths = set()

    import_map = {}
    for import_statement in import_statements:
        target_file = import_statement.root().file
        imports_for_file = import_map.get(target_file, [])
        imports_for_file.append(import_statement)
        import_map[target_file] = imports_for_file

    from grimp.adaptors.graph import ImportGraph

    graph = ImportGraph()
    for import_file in import_map:
        import_file_module_name = _module_name_from_filename(import_file, target_folder)
        graph.add_module(import_file_module_name)

        imports = import_map[import_file]
        for import_statement in imports:
            if isinstance(import_statement, astroid.nodes.Import):
                for name in import_statement.names[0]: # fixme should not just access at 0
                    if name is None:
                        continue
                    graph.add_import(
                        importer=import_file_module_name,
                        imported=name,
                        line_number=import_statement.lineno,
                        line_contents=import_statement.as_string()
                    )
                    pass

            if isinstance(import_statement, astroid.nodes.ImportFrom):

                if import_statement.level is None:
                    imported = import_statement.modname

                    print(f'"{import_file_module_name}" -> "{imported}"')
                    graph.add_import(
                        importer=import_file_module_name,
                        imported=imported,
                        line_number=import_statement.lineno,
                        line_contents=import_statement.as_string()
                    )

                if import_statement.level is not None:
                    importer_parts = import_file_module_name.split(".")
                    import_target_module = importer_parts[0: -1 * import_statement.level] + import_statement.modname.split(".")


                    for name in import_statement.names[0]: # fixme should not just access at 0
                        imported = ".".join(import_target_module)
                        if name is not None:
                            imported = ".".join(import_target_module + [name])

                        print(f'"{import_file_module_name}" -> "{imported}"')
                        graph.add_import(
                            importer=import_file_module_name,
                            imported=imported,
                            line_number=import_statement.lineno,
                            line_contents=import_statement.as_string()
                        )

    yield []


import_graph = Structure("IMPORT_GRAPH", {
})
import_graph.must([])

import_statements = Structure("IMPORT_STATEMENTS", {
        "IMPORT_GRAPH": import_statements_to_graph,
})
import_statements.has([import_graph])

project_files = Structure("ALL_PATHON_FILES",
    {
        "IMPORT_STATEMENTS": files_to_import_graph,
    }
)
project_files.has([import_statements])

project = Structure("PROJECT",
    {
        "ALL_PATHON_FILES": project_to_files,
    }
)
project.has([project_files])

linter = Linter(project)
results = linter.lint(target_folder)

print(list(results))




