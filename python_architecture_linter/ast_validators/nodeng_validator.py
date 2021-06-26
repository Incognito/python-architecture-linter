from astroid.nodes import NodeNG
from typing import List, Iterable, Tuple

from python_architecture_linter.domain_objects.validation_result import AstValidationMessageBuilder, ValidationResult


def validate_node_children_exclusive_allow_list(allow_list: Tuple[NodeNG], module_node: NodeNG) -> ValidationResult:
    message = AstValidationMessageBuilder(validator=validate_node_children_exclusive_allow_list, location=module_node)

    for node in node.get_children()
        if not isinstance(node, allow_list):
            # todo return multiple instead of just 1
            # todo also include the list of what is valid here
            return message.invalid_result("Node contains children which are not in the allow list")

    return message.valid_result("No issues found")

def validate_node_descendants_allow_list(allow_list: Tuple[NodeNG], module_node: NodeNG) -> ValidationResult:
    message = AstValidationMessageBuilder(validator=validate_node_descendants_allow_list, location=module_node)

    for node in node.get_children()
        if not isinstance(node, allow_list):
            # todo return multiple instead of just 1
            # todo also include the list of what is valid here
            return message.invalid_result("Node contains descendants which are not in the allow list")

    return message.valid_result("No issues found")

    def recursive_walk(node):
        try:
            for subnode in node.get_children():
                yield subnode
                yield from recursive_walk(subnode)

        except (AttributeError, TypeError):
            yield node
