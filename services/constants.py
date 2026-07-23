"""Message constants for the in-memory local cart service."""

from enum import StrEnum


class Messages(StrEnum):
    """Log and error messages for ``LocalCart`` operations."""

    EMPTY_CART = "empty cart"
    PRODUCT_ID_NOT_IN_CART = "product id not found in cart"
    POP_LAST_FROM_CART = "pop last item from cart"
