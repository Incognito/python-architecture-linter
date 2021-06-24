import astroid

from python_architecture_linter.domain_objects.validation_result import invalid_result, valid_result, ValidationResult


def class_name_validator(class_node: astroid.nodes.ClassDef) -> ValidationResult:
    if not class_node.name.endswith("Provider"):
        return invalid_result(__file__, "Provider class names must end with the word Provider")
    
    return valid_result(__file__, "Provider class ended with the word Provider")
