from functools import partial
from pathlib import Path
from typing import List

import astroid
from modular_provider_architecture_definition.validators import (
    must_create_few_objects_in_provider_method,
    must_have_no_arguments_in_provider_method,
    must_not_contain_logic,
    must_only_be_in_run_modules,
    must_only_have_provider_in_module_root,
    must_only_import_and_define_classes,
    must_suffix_provider_classes,
    must_use_provider_method_names,
)

from python_architecture_linter.node_navigators import (
    ast_node_to_specific_children,
    file_to_ast,
    project_to_file_filtered,
)
from python_architecture_linter.tree_structure import Structure

provider_ast_method = Structure("PROVIDER_AST_METHOD", {})
provider_ast_method.must(
    [
        must_use_provider_method_names,
        must_create_few_objects_in_provider_method,
        must_have_no_arguments_in_provider_method,
        must_not_contain_logic,
    ]
)

node_to_function_nodes = partial(ast_node_to_specific_children, (astroid.nodes.FunctionDef))
provider_ast_class = Structure("PROVIDER_AST_CLASS", {"PROVIDER_AST_METHOD": node_to_function_nodes})
provider_ast_class.has([provider_ast_method])
provider_ast_class.must([must_suffix_provider_classes])

provider_ast_import = Structure("PROVIDER_AST_IMPORT", {})
provider_ast_import.must(
    [
        # must_only_import_internals_or_other_providers
    ]
)

node_to_import_nodes = partial(ast_node_to_specific_children, (astroid.nodes.Import, astroid.nodes.ImportFrom))
node_to_class_nodes = partial(ast_node_to_specific_children, (astroid.nodes.ClassDef))
provider_ast_module = Structure(
    "PROVIDER_AST_MODULE", {"PROVIDER_AST_CLASS": node_to_class_nodes, "PROVIDER_AST_IMPORT": node_to_import_nodes}
)
provider_ast_module.must([must_only_import_and_define_classes])
provider_ast_module.has([provider_ast_import, provider_ast_class])

provider_file = Structure("PROVIDER_FILE", {"PROVIDER_AST_MODULE": file_to_ast})
provider_file.has([provider_ast_module])

logic_ast_module = Structure("LOGIC_AST_MODULE", {})
logic_ast_module.must(
    [
        # disallow provider imports
    ]
)

logic_file = Structure(
    "LOGIC_FILE",
    {
        "LOGIC_AST_MODULE": file_to_ast,
    },
)
logic_file.has([logic_ast_module])

run_file = Structure("RUN_FILE", {})
run_file.must([must_only_be_in_run_modules])


def filename_filter(file_name: str, path: Path) -> bool:
    return path.name == file_name


def filename_exclusion_filter(file_names: List[str], path: Path) -> bool:
    return path.name not in file_names


run_file_filter = partial(filename_filter, "run.py")
provider_file_filter = partial(filename_filter, "provider.py")
logic_file_filter = partial(filename_exclusion_filter, ["provider.py", "run.py"])

project = Structure(
    "PROJECT",
    {
        "RUN_FILE": partial(project_to_file_filtered, run_file_filter),
        "PROVIDER_FILE": partial(project_to_file_filtered, provider_file_filter),
        "LOGIC_FILE": partial(project_to_file_filtered, logic_file_filter)
        # todo: dependency graph
    },
)
project.must(
    [
        must_only_have_provider_in_module_root,
    ]
)
project.has([provider_file, run_file, logic_file])


project_definition = project
