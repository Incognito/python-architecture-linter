from python_architecture_linter import Linter
from python_architecture_linter_grimp_extension.grimp_definition import project

target_folder = "/home/brian/python-architecture-linter-monorepo/modular_provider_architecture_definition/tests/cases/modular_provider_architecture"


# print statements build the correct dependency model for this project
#
#   "modular_provider_architecture.module_runtime.provider" -> "functools"
#   "modular_provider_architecture.module_runtime.provider" -> "modular_provider_architecture.logic_module.logic"
#   "modular_provider_architecture.module_runtime.provider" -> "modular_provider_architecture.logic_module.provider"
#   "modular_provider_architecture.module_runtime.provider" -> "modular_provider_architecture.module_runtime.runtime"
#   "modular_provider_architecture.module_runtime.run" -> "modular_provider_architecture.module_runtime.provider"
#   "modular_provider_architecture.logic_module.provider" -> "modular_provider_architecture.logic_module.logic"
#
#                     ┌───────────────────────┐
#                     │  module_runtime.run   │
#                     └───────────────────────┘
#                       │
#                       │
#                       ▼
#   ┌───────────┐     ┌────────────────────────────┐     ┌────────────────────────┐
#   │ functools │ ◀── │  module_runtime.provider   │ ──▶ │ module_runtime.runtime │
#   └───────────┘     └────────────────────────────┘     └────────────────────────┘
#                       │                        │
#                       │                        │
#                       ▼                        │
#                     ┌───────────────────────┐  │
#                     │ logic_module.provider │  │
#                     └───────────────────────┘  │
#                       │                        │
#                       │                        │
#                       ▼                        │
#                     ┌───────────────────────┐  │
#                     │  logic_module.logic   │ ◀┘
#                     └───────────────────────┘

linter = Linter(project)
results = linter.lint(target_folder)

print(list(results))
