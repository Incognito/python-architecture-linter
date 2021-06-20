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
from python_architecture_linter.linter import Linter

MODULE_VALIDATORS = [validate_provider_module_contents]
CLASS_VALIDATORS = [class_name_validator]
METHOD_VALIDATORS = [
    method_name_validator,
    method_arguments_validator,
    method_logic_validator,
    method_object_creation_count,
]

provider_class_linter = Linter(
    MODULE_VALIDATORS,
    CLASS_VALIDATORS,
    METHOD_VALIDATORS
)
