"""Example usages for the `validating_base.ValidatingBaseClass` class."""

import pytest
from typeguard import TypeCheckError
from validating_base import ValidatingBaseClass


class ActionExample(ValidatingBaseClass):
    """Shows an example usage of the `validating_base.ValidatingBaseClass` class."""

    required_methods: list[str] = ["action"]
    validated_methods: list[str] = ["action"]

    def validate_action(self, number_list: list[int]) -> None:
        """Validate that the data to be processed is in the correct format.

        Args:
            number_list (List[int]): The list of ints

        Raises:
            TypeError: Raised if the data is not the correct type
            ValueError: Raised if the types are correct, but there is an issue in the formatting
        """
        for number in number_list:
            if not isinstance(number, int):
                raise TypeError(f"{number} is not an integer")


class AdderExample(ActionExample):
    """A class that adds things."""

    def action(self, number_list: list[int]) -> int:
        """Take a list of ints and sum all of the elements.

        The validation method in this case is `ActionExample.validate_action`.

        Args:
            number_list (List[int]): The list of ints

        Returns:
            int: The sum of all elements in the list
        """
        total = 0
        for number in number_list:
            total = total + number

        return total


class MultiplierExample(ActionExample):
    """A class that multiplies things."""

    def action(self, number_list: list[int]) -> int:
        """Take a list of ints and multiply all of the elements.

        The validation method in this case is `ActionExample.validate_action`.

        Args:
            number_list (List[int]): The list of ints

        Returns:
            int: The multiply of all elements in the list
        """
        total = 1
        for number in number_list:
            total = total * number

        return total


class InvalidExample(ActionExample):
    """A class that doesn't define an action method."""


class BaseMissingValidator(ValidatingBaseClass):
    """Needs a validated function but will fail."""

    validated_methods: list[str] = ["action"]


class MissingValidator(BaseMissingValidator):
    """Define the action but not the validator."""

    def action(self, items: dict[str, str]) -> None:
        """Validated."""


class MissingValidatedAction(ValidatingBaseClass):
    """Define the validator but not the action."""

    validated_methods: list[str] = ["action"]

    def validate_action(self, items: dict[str, str]) -> None:
        """Validated."""


class DifferentSignatures(ValidatingBaseClass):
    """Different signatures for action and validator."""

    validated_methods: list[str] = ["action"]

    def action(self, items: dict[str, str]) -> None:
        """Validated."""

    def validate_action(self, items: int) -> None:
        """Validated."""


class ValidatorReturnsNotNone(ValidatingBaseClass):
    """Different signatures for action and validator."""

    validated_methods: list[str] = ["action"]

    def action(self, items: dict[str, str]) -> None:
        """Validated."""

    def validate_action(self, items: dict[str, str]) -> int:  # type: ignore[empty-body]
        """Validated."""


class NonCallableValidator(ValidatingBaseClass):
    """A validator that is not callable."""

    validated_methods: list[str] = ["action"]

    def action(self, items: dict[str, str]) -> None:
        """Validated."""

    validate_action: int = 1


class NonCallableAction(ValidatingBaseClass):
    """An action that is not callable."""

    validated_methods: list[str] = ["action"]

    action: int = 1

    def validate_action(self, items: dict[str, str]) -> None:
        """Validated."""


class RequiredNonCallable(ValidatingBaseClass):
    """A required method that is not callable."""

    required_methods: list[str] = ["action"]

    action: int = 1


def test_adder() -> None:
    """Tests that the adder class gets validated."""
    adder = AdderExample()

    total = adder.action([1, 2, 3, 4, 5])
    assert total == 15

    with pytest.raises(TypeCheckError, match="is not an instance of int"):
        adder.action(["1", 2, 3, 4, 5])  # type: ignore


def test_multiplier() -> None:
    """Tests that the multiplier class gets validated."""
    multiplier = MultiplierExample()

    total = multiplier.action([1, 2, 3, 4, 5])
    assert total == 120

    with pytest.raises(TypeCheckError, match="is not an instance of int"):
        multiplier.action(["1", 2, 3, 4, 5])  # type: ignore


def test_missing_required() -> None:
    """Tests that a class with a missing requirement raises an error."""
    with pytest.raises(NotImplementedError, match="method must be defined"):
        InvalidExample()


def test_missing_validator() -> None:
    """Tests that a class with a missing requirement raises an error."""
    with pytest.raises(NotImplementedError, match="The validate_action method must be defined for the action method."):
        MissingValidator()


def test_missing_validated_action() -> None:
    """Tests that a class with a missing requirement raises an error."""
    with pytest.warns(match="method is not implemented"):
        MissingValidatedAction()


def test_different_signatures() -> None:
    """Tests a validator and an action having different signatures."""
    with pytest.raises(TypeError, match="must have the same argument signature as"):
        DifferentSignatures()


def test_validator_returns_not_none() -> None:
    """Tests a validator returning a value."""
    with pytest.raises(TypeError, match="must have a return type of None"):
        ValidatorReturnsNotNone()


def test_non_callable_validator() -> None:
    """Tests a validator that is not callable."""
    with pytest.raises(TypeError, match="must be a callable"):
        NonCallableValidator()


def test_non_callable_action() -> None:
    """Tests an action that is not callable."""
    with pytest.raises(TypeError, match="must be a callable"):
        NonCallableAction()


def test_required_non_callable() -> None:
    """Tests a required method that is not callable."""
    with pytest.raises(TypeError, match="must be a callable"):
        RequiredNonCallable()