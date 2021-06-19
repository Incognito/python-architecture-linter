import astroid
from functools import partial
from operator import is_not


class Linter:
    def __init__(self, class_validators, method_validators):
        self._class_validators = class_validators
        self._method_validators = method_validators

    def lint(self, code):
        class_node = astroid.extract_node(code)

        messages = []
        for validator in self._class_validators:
            message = validator(class_node)
            messages.append(message)

        for func_node in class_node.body:
            if not isinstance(func_node, astroid.nodes.FunctionDef):
                continue

            for validator in self._method_validators:
                message = validator(func_node)
                messages.append(message)

        return list(filter(partial(is_not, None), messages))
