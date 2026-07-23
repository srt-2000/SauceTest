from enum import StrEnum


class PageLocators(StrEnum):
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


class Messages(StrEnum):
    UNEXPECTED_DATA = "unexpected data"
    INVALID_PRICE_TEXT = "invalid price text"
    MISSING_DATA_TEST = "missing data-test on add button"


class Values(StrEnum):
    ADD_TO_CART_PREFIX = "add-to-cart-"
    DATA_TEST = "data-test"
    INDEX = "index"