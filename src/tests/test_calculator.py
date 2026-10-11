"""
Calculator app tests
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import pytest
from calculator import Calculator


@pytest.fixture
def calculator():
    """
    Provide a new Calculator object to each test that requests it.

    Returns:
        Calculator: a fresh calculator object.
    """
    return Calculator()


def test_app(calculator, tmp_path, monkeypatch):
    """
    Verify that the welcome message shows the user name read from the .env file.
    """
    env_file = tmp_path / ".env"
    env_file.write_text("CALCULATOR_USERNAME=YourName")

    monkeypatch.chdir(tmp_path)
    assert calculator.get_hello_message() == (
        "== Calculatrice v1.0 ==\n"
        "Bienvenu(e) YourName\n"
    )


@pytest.mark.parametrize(
    "value_one, value_two, expected_result",
    [(1, 2, 3), (-4, -6, -10), (0, 0, 0), (0.1, 0.2, pytest.approx(0.3))],
    ids=["positif", "negatif", "zero", "decimal"],
)
def test_addition(calculator, value_one, value_two, expected_result):
    """
    Verify addition and that its result is stored in last_result.
    Decimal results use pytest.approx because 0.1 + 0.2 is not exactly 0.3.
    """
    assert calculator.addition(value_one, value_two) == expected_result
    assert calculator.last_result == expected_result


@pytest.mark.parametrize(
    "value_one, value_two, expected_result",
    [(5, 3, 2), (-3, -5, 2), (0, 0, 0), (0.3, 0.1, pytest.approx(0.2))],
    ids=["positif", "negatif", "zero", "decimal"],
)
def test_subtraction(calculator, value_one, value_two, expected_result):
    """
    Verify subtraction and that its result is stored in last_result.
    """
    assert calculator.subtraction(value_one, value_two) == expected_result
    assert calculator.last_result == expected_result


@pytest.mark.parametrize(
    "value_one, value_two, expected_result",
    [(3, 4, 12), (-3, 4, -12), (7, 0, 0), (0.5, 0.2, pytest.approx(0.1))],
    ids=["positif", "negatif", "zero", "decimal"],
)
def test_multiplication(calculator, value_one, value_two, expected_result):
    """
    Verify multiplication and that its result is stored in last_result.
    """
    assert calculator.multiplication(value_one, value_two) == expected_result
    assert calculator.last_result == expected_result


@pytest.mark.parametrize(
    "value_one, value_two, expected_result",
    [(100, 2, 50), (-9, 3, -3), (0, 5, 0), (2.5, 2, 1.25)],
    ids=["positif", "negatif", "zero", "decimal"],
)
def test_division(calculator, value_one, value_two, expected_result):
    """
    Verify division by a non-zero value and that its result is stored in
    last_result.
    """
    assert calculator.division(value_one, value_two) == expected_result
    assert calculator.last_result == expected_result


@pytest.mark.parametrize("value_two", [0, 0.0], ids=["entier", "decimal"])
def test_division_by_zero(calculator, value_two):
    """
    Verify that dividing by zero does not raise: the calculator returns an
    error message and stores "Error" in last_result.
    """
    assert calculator.division(1, value_two) == "Erreur : division par zéro"
    assert calculator.last_result == "Error"


@pytest.mark.xfail(reason="Q1 : test volontairement en échec, division() ne lève pas ZeroDivisionError")
def test_division_by_zero_should_raise(calculator):
    """
    Intentionally failing test written for Question 1: it expects
    ZeroDivisionError, but the calculator returns a message instead.
    Run `pytest --runxfail -k should_raise` to see how pytest reports it.
    """
    with pytest.raises(ZeroDivisionError):
        calculator.division(1, 0)
