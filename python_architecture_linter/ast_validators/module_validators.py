import astroid

from python_architecture_linter.domain_objects.validation_result import AstValidationMessageBuilder, ValidationResult


def validate_provider_module_contents(module_node: astroid.nodes.Module) -> ValidationResult:
    message = AstValidationMessageBuilder(
        validator=validate_provider_module_contents,
        location=module_node
    )

    # todo duplicate validation from logic allowed in method
    allow_list = (
        astroid.nodes.Import,
        astroid.nodes.ImportFrom,
        astroid.nodes.ClassDef,
    )

    for node in module_node.body:
        if not isinstance(node, allow_list):
            # todo return multiple
            # todo return better explanation with code printout or line numbers
            return message.invalid_result(
                "Provider file contains more than imports and class definitions"
            )

        return message.valid_result("No issues found")
