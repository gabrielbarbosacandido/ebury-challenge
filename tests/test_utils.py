import pytest

from include.utils import validate_date_format


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2025-01-01", True),
        ("2020-12-31", True),
    ],
)
def test_validate_date_format_valid(date_str: str, expected: bool) -> None:
    """
    Test that validates the date format when the input date string is valid.

    Args:
        date_str (str): The date string to validate.
        expected (bool): Expected result (True for valid date).
    """
    result = validate_date_format(date_str)
    assert result == expected


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2025-31-01", False),
        ("2025-02-30", False),
        ("2025-13-01", False),
        ("2025-01-32", False),
        ("2025/01/01", False),
        ("01-01-2025", False),
        ("2025-01-01 10:00", False),
        ("", False),
    ],
)
def test_validate_date_format_invalid(date_str: str, expected: bool) -> None:
    """
    Test that validates the date format when the input date string is invalid.

    Args:
        date_str (str): The date string to validate.
        expected (bool): Expected result (False for invalid date).
    """
    result = validate_date_format(date_str)
    assert result == expected
