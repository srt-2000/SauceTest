from __future__ import annotations

from decimal import Decimal, InvalidOperation
from loguru import logger

from page_handlers.constants import Messages, Values


def handle_str_to_decimal(raw_value: str) -> Decimal:
    """Convert a price label like '$29.99' to Decimal."""
    normalized_number_value: str = raw_value.replace("$", "").strip()

    try:
        return Decimal(normalized_number_value)
    except InvalidOperation as error:
        logger.error(f"{Messages.INVALID_PRICE_TEXT}: {raw_value!r}")
        raise ValueError from error


def get_product_slug(data: str) -> str:
    """Extract product slug from add-to-cart data-test attribute."""
    target_prefix: str = Values.ADD_TO_CART_PREFIX

    if not data.startswith(target_prefix):
        logger.error(f"{Messages.UNEXPECTED_DATA}: {data!r}")
        raise ValueError

    return data.removeprefix(target_prefix)
