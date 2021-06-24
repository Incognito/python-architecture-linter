from __future__ import annotations

import astroid

class StructureWalker:
    def walk_requirements(self, structure: Structure):
        self._requirement_walker(structure)

    def _requirement_walker(self):
        # fixme, accesses private
        for requirement in project_structure._validators:
            requirement

        for requirement in project_structure._must_have:
            requirement

        for requirement in project_structure._may_have:
            requirement

        for requirement in project_structure._must_not_have:
            requirement

from python_architecture_linter.ast_validators.module_validators import (validate_provider_module_contents)
from python_architecture_linter.ast_validators.class_validators import (
    class_name_validator,
)
from python_architecture_linter.ast_validators.method_validators import (
    method_arguments_validator,
    method_logic_validator,
    method_name_validator,
    method_object_creation_count,
)

provider_method = Structure()
provider_method.requires([
        method_name_validator,
        method_arguments_validator,
        method_logic_validator,
        method_object_creation_count,
    ])

provider_class = Structure()
provider_class.requires([class_name_validator])
provider_class.may_have([provider_method])

module_imports = Structure()
module_imports.requires([])

provider_file = Structure()
provider_file.requires([
        validate_provider_module_contents,
     ])

provider_file.may_have([
        module_imports,
        provider_class
    ])
    
module_folders = Structure()
module_folders.must_not_have([module_folders]) # self-reference
module_folders.may_have([provider_file])

run_file = Structure()
run_file.may_have([]) # tbd

runtime_module_folders = Structure()
runtime_module_folders.must_have([run_file])

project = Structure()
project.must_have([module_folders])
project.may_have([runtime_module_folders])



converters = [
    project_to_files
    files_to_module_ast
    module_ast_to_classes
    classes_to_methods
]
