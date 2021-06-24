import astroid
from typing import List

from python_architecture_linter.domain_objects.validation_result import ValidationResult

# todo this class is mixing validation and navigation together
class Linter:
    def __init__(self, module_validators, class_validators, method_validators):
        self._module_validators = module_validators
        self._class_validators = class_validators
        self._method_validators = method_validators

    def lint(self, module_node: astroid.nodes.Module) -> List[ValidationResult]:
        messages = []

        for validator in self._module_validators:
            # todo check if there are import rules too
            message = validator(module_node)
            messages.append(message)


        provider_classes = filter(lambda node: isinstance(node, astroid.nodes.ClassDef), module_node.body)
        # todo move out to own abstraction
        for provider_class in provider_classes:

            for validator in self._class_validators:
                message = validator(provider_class)
                messages.append(message)

            for func_node in provider_class.body:
                if not isinstance(func_node, astroid.nodes.FunctionDef):
                    continue

                for validator in self._method_validators:
                    message = validator(func_node)
                    messages.append(message)

        return messages
