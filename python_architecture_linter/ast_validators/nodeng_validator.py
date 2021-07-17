from typing import Iterable, Tuple

import astroid

from python_architecture_linter.domain_objects.validation_result import (
    AstValidationResultBuilder,
    ValidationResult,
)


def validate_node_children_exclusive_allow_list(
    allow_list: Tuple[astroid.node_classes.NodeNG], node: astroid.node_classes.NodeNG
) -> ValidationResult:
    message = AstValidationResultBuilder(validator=validate_node_children_exclusive_allow_list, location=node)

    unallowed_nodes = [
        node
        for node in node.get_children()
        if not isinstance(node, allow_list)
    ]

    if unallowed_nodes:
        explanation = "Node contains children which are not in the allow list\n"
        for unallowed_node in unallowed_nodes:
            explanation += f"- found '{type(unallowed_node).__name__}'  on line {unallowed_node.lineno},   column {unallowed_node.col_offset}: \n"

        return message.invalid_result(explanation)

    return message.valid_result("No issues found")


def validate_node_descendants_allow_list(
    allow_list: Tuple[astroid.node_classes.NodeNG], node: astroid.node_classes.NodeNG
) -> ValidationResult:
    message = AstValidationResultBuilder(validator=validate_node_descendants_allow_list, location=node)

    unallowed_nodes = [
        node
        for node in node.get_children()
        if not isinstance(node, allow_list)
    ]

    if unallowed_nodes:
        explanation = "Node contains descendants which are not in the allow list\n"
        for unallowed_node in unallowed_nodes:
            explanation += f"- found '{type(unallowed_node).__name__}'  on line {unallowed_node.lineno},   column {unallowed_node.col_offset}: \n"

        return message.invalid_result(explanation)

    return message.valid_result("No issues found")


# todo this doesn't really belong in "validators", probably better as a navigator.
def recursive_walk(node: astroid.node_classes.NodeNG) -> Iterable[astroid.node_classes.NodeNG]:
    try:
        for subnode in node.get_children():
            yield subnode
            yield from recursive_walk(subnode)

    except (AttributeError, TypeError):
        yield node
