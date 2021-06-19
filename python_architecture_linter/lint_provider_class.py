from python_architecture_linter.class_validators import class_name_validator

CLASS_VALIDATORS = [class_name_validator]

from python_architecture_linter.method_validators import (
    method_name_validator,
    method_arguments_validator,
    method_logic_validator,
    method_object_creation_count,
)

METHOD_VALIDATORS = [
    method_name_validator,
    method_arguments_validator,
    method_logic_validator,
    method_object_creation_count,
]


from python_architecture_linter.linter import Linter

linter = Linter(CLASS_VALIDATORS, METHOD_VALIDATORS)
