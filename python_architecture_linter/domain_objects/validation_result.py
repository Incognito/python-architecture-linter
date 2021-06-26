from dataclasses import dataclass


# fixme, ValidationResult or ValidationMessage?
@dataclass(frozen=True)
class ValidationResult:
    explanation: str
    is_valid: bool
    location: str
    validator: str


# todo make a base class for other message builders
class AstValidationMessageBuilder:
    def __init__(self, validator, location):
        self._validator = validator
        self._location = self._location_node_to_string(location)

    def _location_node_to_string(self, location_node) -> str:
        return ":".join([location_node.root().file, str(location_node.fromlineno)])

    def _validation_factory(self, is_valid, validator, location, explanation) -> ValidationResult:
        validator_as_string = ".".join([validator.__module__, validator.__name__])
        result = ValidationResult(
            explanation=explanation,
            is_valid=is_valid,
            location=location,
            validator=validator_as_string,
        )

        return result

    def invalid_result(self, explanation) -> ValidationResult:
        return self._validation_factory(False, self._validator, self._location, explanation)

    def valid_result(self, explanation) -> ValidationResult:
        return self._validation_factory(True, self._validator, self._location, explanation)
