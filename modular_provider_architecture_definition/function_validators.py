import astroid

from typing import Tuple

from python_architecture_linter.domain_objects.validation_result import AstValidationMessageBuilder, ValidationResult


# todo move to project definition
def method_arguments_validator(func_node: astroid.nodes.FunctionDef) -> ValidationResult:
    message = AstValidationMessageBuilder(validator=method_arguments_validator, location=func_node)

    if func_node.name.startswith(("provide_", "_provide_")):
        if not func_node.args.as_string() == "self":
            return message.invalid_result(
                f"invalid arguments in method name {func_node.name}({func_node.args.as_string()}), should only receive self",
            )
    return message.valid_result("No issues found")


# todo move to project definition
def method_object_creation_count(func_node: astroid.nodes.FunctionDef) -> ValidationResult:
    message = AstValidationMessageBuilder(validator=method_object_creation_count, location=func_node)

    creational_call_count = 0
    for node in recursive_walk(func_node):
        if isinstance(node, astroid.nodes.Call):
            function_path = node.func.as_string()
            if not (function_path.startswith("self.") or function_path.endswith("Provider")):
                creational_call_count += 1

    if creational_call_count > 2:
        return message.invalid_result(
            f"Too many business objects are created in {func_node.name}. This would create tight-coupling of object creation, which the provider aims to avoid",
        )

    return message.valid_result("No issues found")
