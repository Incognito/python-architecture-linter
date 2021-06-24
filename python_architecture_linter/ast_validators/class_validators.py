import astroid

from python_architecture_linter.domain_objects.validation_result import AstValidationMessageBuilder, ValidationResult


def class_name_validator(class_node: astroid.nodes.ClassDef) -> ValidationResult:
    message = AstValidationMessageBuilder(
        validator=class_name_validator,
        location=class_node
    )

    if not class_node.name.endswith("Provider"):
        return message.invalid_result(
               "Provider class names must end with the word Provider")

    return message.valid_result("No issues found")
