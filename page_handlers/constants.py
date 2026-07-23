"""CSS / data-test locators and shared page-handler constants."""

from enum import StrEnum, IntEnum


class PageLocators(StrEnum):
    """Playwright selectors for SauceDemo pages."""

    USERNAME = "[data-test='username']"
    PASSWORD = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    INVENTORY_LIST = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_DESCRIPTION = ".inventory_item_desc"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    SHOPPING_CART_BADGE = "[data-test='shopping-cart-badge']"
    ADD_TO_CART = "button[data-test^='add-to-cart-']"
    SHOPPING_CART_LINK = "[data-test='shopping-cart-link']"
    CART_ITEM = ".cart_item"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CHECKOUT_INFO = ".checkout_info"
    FIRST_NAME = "[data-test='firstName']"
    LAST_NAME = "[data-test='lastName']"
    POSTAL_CODE = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    SUMMARY_INFO = ".summary_info"
    PAYMENT_INFO_VALUE = "[data-test='payment-info-value']"
    SHIPPING_INFO_VALUE = "[data-test='shipping-info-value']"
    TAX_LABEL = "[data-test='tax-label']"
    TOTAL_LABEL = "[data-test='total-label']"
    FINISH_BUTTON = "[data-test='finish']"
    COMPLETE_HEADER = "[data-test='complete-header']"
    GENERATE_PDF_BUTTON = "text=Generate PDF order"
    CART_QUANTITY = ".cart_quantity"
    ITEM_TOTAL_LABEL = "[data-test='subtotal-label']"


class Messages(StrEnum):
    """Error messages for page handlers and price-parsing helpers."""

    UNEXPECTED_DATA = "unexpected data"
    INVALID_PRICE_TEXT = "invalid price text"
    MISSING_DATA_TEST = "missing data-test on add button"
    PRODUCT_NOT_IN_LOCAL_CART = "overview product not found in local cart"


class Values(StrEnum):
    """Literal prefixes and tokens used when parsing page attributes."""

    ADD_TO_CART_PREFIX = "add-to-cart-"
    REMOVE_PREFIX = "remove-"
    DATA_TEST = "data-test"
    INDEX = "index"
    DOLLAR = "$"
    EMPTY = ""


class IntValues(IntEnum):
    """Integer indices used when splitting labeled price strings."""

    PRICE_VALUE_INDEX = 1
