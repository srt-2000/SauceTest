"""Helpers for parsing inventory prices and product slugs."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from loguru import logger

from page_handlers.constants import Messages, Values, IntValues


def handle_str_to_decimal(raw_value: str) -> Decimal:
    """Convert a price label like ``$29.99`` to ``Decimal``.

    Args:
        raw_value: Raw price text from the page (may include ``$``).

    Returns:
        Parsed monetary amount.

    Raises:
        ValueError: If ``raw_value`` is not a valid decimal after cleanup.
    """
    normalized_number_value: str = raw_value.replace(
        Values.DOLLAR, Values.EMPTY
    ).strip()

    try:
        return Decimal(normalized_number_value)
    except InvalidOperation as error:
        logger.error(f"{Messages.INVALID_PRICE_TEXT}: {raw_value!r}")
        raise ValueError from error


def get_product_slug(data: str) -> str:
    """Extract product slug from an add-to-cart ``data-test`` attribute.

    Args:
        data: Full ``data-test`` value, e.g. ``add-to-cart-sauce-labs-backpack``.

    Returns:
        Product slug without the add-to-cart prefix.

    Raises:
        ValueError: If ``data`` does not start with the expected prefix.
    """
    target_prefix: str = Values.ADD_TO_CART_PREFIX

    if not data.startswith(target_prefix):
        logger.error(f"{Messages.UNEXPECTED_DATA}: {data!r}")
        raise ValueError

    return data.removeprefix(target_prefix)


def to_clear_labeled_price_to_decimal_digit(raw_value: str) -> Decimal:
    """Parse labeled price text such as ``Tax: $2.40`` to ``Decimal``.

    Args:
        raw_value: Labeled amount from overview (must contain ``$``).

    Returns:
        Parsed monetary amount after the dollar sign.

    Raises:
        ValueError: If ``raw_value`` has no ``$`` or is not a valid decimal.
    """
    if Values.DOLLAR not in raw_value:
        raise ValueError(f"{Messages.INVALID_PRICE_TEXT}: {raw_value!r}")

    cleared_price: str = raw_value.split(
        sep=Values.DOLLAR,
        maxsplit=1
    )[IntValues.PRICE_VALUE_INDEX].strip()

    return handle_str_to_decimal(f"{Values.DOLLAR}{cleared_price}")
