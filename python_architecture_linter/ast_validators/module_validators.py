import astroid

from python_architecture_linter.domain_objects.validation_result import invalid_result, valid_result, ValidationResult


def validate_provider_module_contents(func_node: astroid.nodes.Module) -> ValidationResult:

    # todo duplicate validation from logic allowed in method
    allow_list = (
        astroid.nodes.Import,
        astroid.nodes.ImportFrom,
        astroid.nodes.ClassDef,
    )

    for node in func_node.body:
        if not isinstance(node, allow_list):
            # todo return multiple
            # todo return better explanation with code printout or line numbers
            return invalid_result(
                __file__,
                "Providers are only intended to wire together things that exist. Anything other than importing and connecting some code with other code is a convention violation for providers",
            )

        return valid_result(__file__, "Provider file only contains a provider")

