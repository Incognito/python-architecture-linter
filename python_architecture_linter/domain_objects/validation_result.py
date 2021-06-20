from dataclasses import dataclass
from functools import partial


@dataclass(frozen=True)
class ValidatiorExplanation:
    # TODO model it so any data format could end up being supported here
    message: str


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    validator: str
    explanation: ValidatiorExplanation


def validation_factory(is_valid, validator, explanation_message):
    explanation = ValidatiorExplanation(message=explanation_message)
    result = ValidationResult(is_valid=is_valid, validator=validator, explanation=explanation)

    return result


invalid_result = partial(validation_factory, False)
valid_result = partial(validation_factory, True)
