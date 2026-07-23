"""Shared application constants for logging, env keys, and Playwright."""

from enum import StrEnum
from typing import Literal


DOM_CONTENT_LOADED: Literal["domcontentloaded"] = "domcontentloaded"


class Messages(StrEnum):
    """Log and error message templates used across the app."""

    MISSING_REQUIRES_VAR = "missing required env var"
    CONFIG_VALUE_ERROR = "CONFIG_VALUE_ERROR"
    PREPARE_FOR_LOGIN = "Prepare for login"
    LOGGED = "Logged"
    ADDED_ITEMS = "Added items to cart in resource and get a local_cart"
    POP_ITEM_FROM_CART = "Removed product in local_cart and get removed_slug"
    OPENED_CART = "Opened cart on resource"
    REMOVED_PRODUCT_ON_WEB = "Removed product from cart on resource"
    CHECKED_CARTS_SYNC = "Checked sync resource and local carts"
    CHECKOUT = "Checkout resource cart"


class Fields(StrEnum):
    """Environment variable names expected in ``.env``."""

    STANDARD_USER = "STANDARD_USER"
    PASSWORD = "PASSWORD"
    RESOURCE_URL = "RESOURCE_URL"


class Values(StrEnum):
    """Shared literal values (e.g. Playwright test-id attribute name)."""

    DATA_TEST = "data-test"
