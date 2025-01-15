from datetime import datetime


def validate_date_format(date_str: str) -> bool:
    """
    Validate if the given date string is in the correct 'YYYY-MM-DD' format.

    Args:
        date_str (str): The date string to be validated.

    Returns:
        bool: True if the date string matches the 'YYYY-MM-DD' format, False otherwise.

    Example:
        >>> _validate_date_format("2025-01-01")
        True

        >>> _validate_date_format("2025-31-01")
        False
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_date_range(from_date: str, to_date: str) -> None:
    """
    Validates that the from_date and to_date are in the correct format
    and ensures both are provided when catchup is True.

    Parameters:
        from_date (str): The start date in 'YYYY-MM-DD' format.
        to_date (str): The end date in 'YYYY-MM-DD' format.

    Raises:
        ValueError: If the dates are in an invalid format or one of them is missing.
    """
    if not from_date or not to_date:
        raise ValueError("Both from_date and to_date are required.")

    if not validate_date_format(from_date):
        raise ValueError(
            f"Invalid from_date format. Expected 'YYYY-MM-DD', got {from_date}."
        )

    if not validate_date_format(to_date):
        raise ValueError(
            f"Invalid to_date format. Expected 'YYYY-MM-DD', got {to_date}."
        )
