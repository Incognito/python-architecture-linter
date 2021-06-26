import astroid

from typing import Tuple

from python_architecture_linter.domain_objects.validation_result import AstValidationMessageBuilder, ValidationResult


def method_name_prefix_validator(prefixes: Tuple[str], func_node: astroid.nodes.FunctionDef) -> ValidationResult:
    message = AstValidationMessageBuilder(validator=method_name_validator, location=func_node)

    if not func_node.name.startswith(("provide_", "_provide_", "_create_", "__init__")):
        return message.invalid_result(
            'Invalid method name {func_node.name}, found one of "provide_", "_provide_", "_create_", "__init__"'
        )

    return message.valid_result("No issues found")
