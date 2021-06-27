from typing import Tuple

import astroid

from python_architecture_linter.domain_objects.validation_result import (
    AstValidationResultBuilder,
    ValidationResult,
)


def method_name_prefix_validator(prefixes: Tuple[str], func_node: astroid.nodes.FunctionDef) -> ValidationResult:
    message = AstValidationResultBuilder(validator=method_name_prefix_validator, location=func_node)

    if not func_node.name.startswith(prefixes):
        return message.invalid_result(
            'Invalid method name {func_node.name}, found one of "provide_", "_provide_", "_create_", "__init__"'
        )

    return message.valid_result("No issues found")
