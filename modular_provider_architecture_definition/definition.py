import astroid
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
)
from python_architecture_linter.tree_structure import Structure

provider_ast_method = Structure("PROVIDER_AST_METHOD", {})
provider_ast_method.must(
    [
        must_use_provider_method_names,
    ]
)

provider_ast_class = Structure("PROVIDER_AST_CLASS", {"PROVIDER_AST_METHOD": lambda x: x})  # todo
provider_ast_class.must([must_suffix_provider_classes])

provider_ast_import = Structure("PROVIDER_AST_IMPORT", {})
provider_ast_import.must([must_only_import_internals_or_other_providers])

provider_ast_module = Structure(
    "PROVIDER_AST_MODULE", {"PROVIDER_AST_CLASS": lambda x: x, "PROVIDER_AST_IMPORT": lambda x: x}  # todo  # todo
)
provider_ast_module.must([must_only_import_and_define_classes])
provider_ast_module.has([provider_ast_import, provider_ast_class])

provider_files = Structure("PROVIDER_FILES", {"PROVIDER_AST": lambda x: x})
provider_files.must([must_only_have_provider_in_module_root])

logic_ast_module = Structure("LOGIC_AST_MODULE", {})
logic_ast_module.must([must_not_create_instances_except_dataclasses])

run_files = Structure(
    "LOGIC_FILES",
    {
        "LOGIC_AST_MODULE": lambda x: x,  # todo make a filter
    },
)
run_files.must([must_only_be_in_modules])

run_files = Structure("RUN_FILES", {})
run_files.must([must_only_be_in_run_modules])

files = Structure(
    "FILES",
    {
        "RUN_FILES": lambda x: x,  # todo make a filter
        "PROVIDER_FILES": lambda x: x,  # todo make a filter
        "LOGIC_FILES": lambda x: x,  # todo make a filter # exclude providers and runtimes
    },
)
files.has(
    [
        run_files,
        provider_files,
        # logic_files # todo
    ]
)
files.must([must_have_modular_folders])

project = Structure(
    "PROJECT",
    {
        "FILES": project_to_files
        # todo: dependency graph
    },
)
project.must([])
project.has([files])
