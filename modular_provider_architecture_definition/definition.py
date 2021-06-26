import astroid

from python_architecture_linter.tree_structure.structure import Structure

from python_architecture_linter.ast_validators.module_validators import validate_provider_module_contents
from python_architecture_linter.ast_validators.class_validators import (
    class_name_validator,
)
from python_architecture_linter.ast_validators.method_validators import (
    method_arguments_validator,
    method_logic_validator,
    method_name_validator,
    method_object_creation_count,
)


def must_only_be_in_run_modules():
    pass


def must_have_modular_folders():
    pass

def must_only_import_internals_or_other_providers():
    pass

def must_not_create_instances_except_dataclasses():
    pass

def must_only_be_in_modules():
    pass


provider_ast_method = Structure("PROVIDER_AST_METHOD", {})
provider_ast_method.must(
    [
        method_name_validator,
        method_arguments_validator,
        method_logic_validator,
        method_object_creation_count,
    ]
)

provider_ast_class = Structure("PROVIDER_AST_CLASS", {"PROVIDER_AST_METHOD": lambda x: x})  # todo
provider_ast_class.must([class_name_validator])

provider_ast_import = Structure("PROVIDER_AST_IMPORT", {})
provider_ast_import.must([must_only_import_internals_or_other_providers])

provider_ast_module = Structure(
    "PROVIDER_AST_MODULE", {"PROVIDER_AST_CLASS": lambda x: x, "PROVIDER_AST_IMPORT": lambda x: x}  # todo  # todo
)
provider_ast_module.must([validate_provider_module_contents])
provider_ast_module.has([provider_ast_import, provider_ast_class])

provider_files = Structure("PROVIDER_FILES", {"PROVIDER_AST": file_to_provider_ast})
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
