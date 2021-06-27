import astroid

from python_architecture_linter.domain_objects.validation_result import (
    AstValidationResultBuilder,
    ValidationResult,
)


def class_name_suffix_validator(suffix: str, class_node: astroid.nodes.ClassDef) -> ValidationResult:
    message = AstValidationResultBuilder(validator=class_name_suffix_validator, location=class_node)

    if not class_node.name.endswith(suffix):
        return message.invalid_result(f"This '{class_node.name}' class MUST end with {suffix}")

    return message.valid_result("No issues found")
