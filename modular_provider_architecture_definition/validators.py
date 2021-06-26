from functools import partial
from typing import Tuple, Iterable, List

import astroid

from python_architecture_linter.domain_objects.file import File
from python_architecture_linter.domain_objects.validation_result import ValidationResult

from python_architecture_linter.ast_validators.class_validators import (
    class_name_suffix_validator,
)
from python_architecture_linter.ast_validators.function_validators import (
    method_name_prefix_validator,
)
from python_architecture_linter.ast_validators.nodeng_validator import (
    validate_node_children_exclusive_allow_list,
    validate_node_descendants_allow_list,
)
from python_architecture_linter.domain_objects.validation_result import (
    AstValidationMessageBuilder,
    ValidationResult,
)


def must_only_have_provider_in_module_root(fixme) -> ValidationResult:
    return ValidationResult(
        explanation="No issues found",
        is_valid=True,
        location="fixme",
        validator="fixme",
    )


def must_only_be_in_run_modules(fixme) -> ValidationResult:
    return ValidationResult(
        explanation="No issues found",
        is_valid=True,
        location="fixme",
        validator="fixme",
    )


def must_have_modular_folders(files: List[File]) -> ValidationResult:
    return ValidationResult(
        explanation="No issues found",
        is_valid=True,
        location="fixme",
        validator="fixme",
    )


def must_only_import_internals_or_other_providers(fixme) -> ValidationResult:
    return ValidationResult(
        explanation="No issues found",
        is_valid=True,
        location="fixme",
        validator="fixme",
    )


def must_not_create_instances_except_dataclasses(fixme) -> ValidationResult:
    return ValidationResult(
        explanation="No issues found",
        is_valid=True,
        location="fixme",
        validator="fixme",
    )


def must_only_be_in_modules(fixme) -> ValidationResult:
    return ValidationResult(
        explanation="No issues found",
        is_valid=True,
        location="fixme",
        validator="fixme",
    )


must_use_provider_method_names = partial(
    method_name_prefix_validator, ("provide_", "_provide_", "_create_", "__init__")
)
must_suffix_provider_classes = partial(class_name_suffix_validator, "Provider")

must_only_import_and_define_classes = partial(
    validate_node_descendants_allow_list,
    (
        astroid.nodes.Import,
        astroid.nodes.ImportFrom,
        astroid.nodes.ClassDef,
    ),
)

must_not_contain_logic = partial(
    validate_node_children_exclusive_allow_list,
    (
        astroid.nodes.AnnAssign,
        astroid.nodes.Assign,
        astroid.nodes.AssignAttr,
        astroid.nodes.AssignName,
        astroid.nodes.Call,
        astroid.nodes.Const,
        astroid.nodes.Dict,
        astroid.nodes.Ellipsis,
        astroid.nodes.EmptyNode,
        astroid.nodes.ExtSlice,
        astroid.nodes.List,
        astroid.nodes.Name,
        astroid.nodes.Pass,
        astroid.nodes.Return,
        astroid.nodes.Set,
        astroid.nodes.SetComp,
        astroid.nodes.Slice,
        astroid.nodes.Starred,
        astroid.nodes.Subscript,
        astroid.nodes.Tuple,
        astroid.nodes.UnaryOp,
    ),
)


def must_have_no_arguments_in_provider_method(func_node: astroid.nodes.FunctionDef) -> ValidationResult:
    message = AstValidationMessageBuilder(validator=must_have_no_arguments_in_provider_method, location=func_node)

    if func_node.name.startswith(("provide_", "_provide_")):
        if not func_node.args.as_string() == "self":
            return message.invalid_result(
                f"invalid arguments in method name {func_node.name}({func_node.args.as_string()}), should only receive self",
            )
    return message.valid_result("No issues found")


def must_create_few_objects_in_provider_method(func_node: astroid.nodes.FunctionDef) -> ValidationResult:
    message = AstValidationMessageBuilder(validator=must_create_few_objects_in_provider_method, location=func_node)

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

    def recursive_walk(node: astroid.node_classes.NodeNG) -> Iterable[astroid.node_classes.NodeNG]:
        try:
            for subnode in node.get_children():
                yield subnode
                yield from recursive_walk(subnode)

        except (AttributeError, TypeError):
            yield node
