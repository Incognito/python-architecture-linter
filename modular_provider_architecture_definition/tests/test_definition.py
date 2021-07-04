import os

from modular_provider_architecture_definition import project_definition

from python_architecture_linter import Linter
from python_architecture_linter.domain_objects.validation_result import ValidationResult


def test_definition():
    path = os.path.dirname(os.path.realpath(__file__)) + "/cases/modular_provider_architecture"  # noqa: E501
    linter = Linter(project_definition)
    results = list(linter.lint(path))

    assert results == [
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "",
            validator="must_only_have_provider_in_module_root",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:0",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_children_exclusive_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:9",
            validator="python_architecture_linter.ast_validators.class_validators.class_name_suffix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:10",
            validator="python_architecture_linter.ast_validators.function_validators.method_name_prefix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:10",
            validator="modular_provider_architecture_definition.validators.must_create_few_objects_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:10",
            validator="modular_provider_architecture_definition.validators.must_have_no_arguments_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:10",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:16",
            validator="python_architecture_linter.ast_validators.function_validators.method_name_prefix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:16",
            validator="modular_provider_architecture_definition.validators.must_create_few_objects_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:16",
            validator="modular_provider_architecture_definition.validators.must_have_no_arguments_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:16",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:19",
            validator="python_architecture_linter.ast_validators.function_validators.method_name_prefix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:19",
            validator="modular_provider_architecture_definition.validators.must_create_few_objects_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:19",
            validator="modular_provider_architecture_definition.validators.must_have_no_arguments_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:19",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:23",
            validator="python_architecture_linter.ast_validators.function_validators.method_name_prefix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:23",
            validator="modular_provider_architecture_definition.validators.must_create_few_objects_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:23",
            validator="modular_provider_architecture_definition.validators.must_have_no_arguments_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/provider.py:23",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:0",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_children_exclusive_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:4",
            validator="python_architecture_linter.ast_validators.class_validators.class_name_suffix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:5",
            validator="python_architecture_linter.ast_validators.function_validators.method_name_prefix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:5",
            validator="modular_provider_architecture_definition.validators.must_create_few_objects_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:5",
            validator="modular_provider_architecture_definition.validators.must_have_no_arguments_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:5",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:8",
            validator="python_architecture_linter.ast_validators.function_validators.method_name_prefix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:8",
            validator="modular_provider_architecture_definition.validators.must_create_few_objects_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:8",
            validator="modular_provider_architecture_definition.validators.must_have_no_arguments_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:8",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:11",
            validator="python_architecture_linter.ast_validators.function_validators.method_name_prefix_validator",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:11",
            validator="modular_provider_architecture_definition.validators.must_create_few_objects_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:11",
            validator="modular_provider_architecture_definition.validators.must_have_no_arguments_in_provider_method",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/logic_module/provider.py:11",
            validator="python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list",
        ),
        ValidationResult(
            explanation="No issues found",
            is_valid=True,
            location=path + "/modular_provider_architecture/module_runtime/run.py",
            validator="must_only_be_in_run_modules",
        ),
    ]
