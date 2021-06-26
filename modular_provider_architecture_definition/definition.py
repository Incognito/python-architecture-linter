import astroid
from functools import partial
from modular_provider_architecture_definition.validators import (
    must_create_few_objects_in_provider_method,
    must_have_modular_folders,
    must_have_no_arguments_in_provider_method,
    must_not_contain_logic,
    must_not_create_instances_except_dataclasses,
    must_only_be_in_modules,
    must_only_be_in_run_modules,
    must_only_have_provider_in_module_root,
    must_only_import_and_define_classes,
    must_only_import_internals_or_other_providers,
    must_suffix_provider_classes,
    must_use_provider_method_names,
)

from python_architecture_linter.node_navigators import (
    ast_node_to_specific_children,
    file_to_ast,
    project_to_files,
    project_to_file,
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

node_to_function_nodes = partial(ast_node_to_specific_children, (astroid.nodes.ClassDef))
provider_ast_class = Structure("PROVIDER_AST_CLASS", {"PROVIDER_AST_METHOD": node_to_function_nodes})
provider_ast_class.must([must_suffix_provider_classes])
provider_ast_class.has([provider_ast_method])

provider_ast_import = Structure("PROVIDER_AST_IMPORT", {})
provider_ast_import.must([must_only_import_internals_or_other_providers])

node_to_import_nodes = partial(ast_node_to_specific_children, (astroid.nodes.Import, astroid.nodes.ImportFrom))
node_to_class_nodes = partial(ast_node_to_specific_children, (astroid.nodes.ClassDef))
provider_ast_module = Structure(
    "PROVIDER_AST_MODULE", {"PROVIDER_AST_CLASS": node_to_class_nodes, "PROVIDER_AST_IMPORT": node_to_import_nodes}
)
provider_ast_module.must([must_only_import_and_define_classes])
provider_ast_module.has([provider_ast_import, provider_ast_class])

provider_file = Structure("PROVIDER_FILE", {"PROVIDER_AST_MODULE": file_to_ast})
provider_file.must([must_only_have_provider_in_module_root])
provider_file.has([provider_ast_module])

logic_ast_module = Structure("LOGIC_AST_MODULE", {})
logic_ast_module.must([must_not_create_instances_except_dataclasses])

logic_file = Structure(
    "LOGIC_FILE",
    {
        "LOGIC_AST_MODULE": file_to_ast,
    },
)
logic_file.must([must_only_be_in_modules])

run_file = Structure("RUN_FILE", {})
run_file.must([must_only_be_in_run_modules])

all_files = Structure("ALL_FILES", {})
all_files.must([must_have_modular_folders])

project = Structure(
    "PROJECT",
    {
        "ALL_FILES": project_to_files,
        "RUN_FILE": project_to_file,  # todo make a filter
        "PROVIDER_FILE": project_to_file,  # todo make a filter
        "LOGIC_FILE": project_to_file,  # todo make a filter # exclude providers and runtimes
        # todo: dependency graph
    },
)
project.must([])
project.has([
    all_files,
    provider_file,
    #run_file,
    #logic_file
])
