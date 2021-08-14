from grimp_package_metrics import dependency_cycles, get_all_package_metrics

from python_architecture_linter import Structure
from python_architecture_linter.domain_objects.validation_result import ValidationResult
from python_architecture_linter.node_navigators import project_to_files
from python_architecture_linter_grimp_extension.grimp_navigators import (
    files_to_import_statements,
    import_statements_to_graph,
)


def must_not_have_modules_depend_on_less_stable_modules(graph) -> ValidationResult:
    package_metrics = {}
    for metric in get_all_package_metrics(graph):
        package_metrics[metric.package_name] = metric

    explanation = ""
    is_valid = (True,)
    for module in graph.modules:
        target_module_instability = package_metrics[module].instability

        modules_importing_target = graph.find_modules_directly_imported_by(module)
        for dependant_module in modules_importing_target:
            dependant_module_instability = package_metrics[dependant_module].instability

            if dependant_module_instability < target_module_instability:
                is_valid = False
                explanation += f"{module}({target_module_instability}) uses less-stable {dependant_module}({dependant_module_instability})\n"

    return ValidationResult(
        explanation=explanation,
        is_valid=is_valid,
        location="project import graph",
        validator="must_not_have_modules_depend_on_less_stable_modules",
    )


def must_not_have_cyclical_imports(graph) -> ValidationResult:
    has_no_cycle = True
    explanation = ""
    for cycle in dependency_cycles(graph):
        has_no_cycle = False
        explanation += str(cycle)

    return ValidationResult(
        explanation=explanation,
        is_valid=has_no_cycle,
        location="Project import graph",
        validator="must_not_have_cyclical_imports",
    )


import_graph = Structure("IMPORT_GRAPH", {})
import_graph.must([must_not_have_cyclical_imports, must_not_have_modules_depend_on_less_stable_modules])


import_statements = Structure("IMPORT_STATEMENTS", {"IMPORT_GRAPH": import_statements_to_graph})
import_statements.has([import_graph])


project_files = Structure("ALL_PATHON_FILES", {"IMPORT_STATEMENTS": files_to_import_statements})
project_files.has([import_statements])


project = Structure("PROJECT", {"ALL_PATHON_FILES": project_to_files})
project.has([project_files])
