"""Inventory page: select all products and capture their data."""
from __future__ import annotations

from playwright.sync_api import Page, expect, Locator
from loguru import logger

from domains import SelectedProduct
from page_handlers.constants import PageLocators, Values, Messages
from page_handlers.utils import handle_str_to_decimal, get_product_slug


class InventoryPage:
    """Inventory grid interactions for SauceDemo."""

    def __init__(self, page: Page) -> None:
        """Bind Playwright page instance."""
        self._page = page

    def add_all_products_to_cart_and_collect_cart_locally(self) -> dict[str, SelectedProduct]:
        """Add every inventory item to cart; return id → product map."""
        items: Locator = self._page.locator(PageLocators.INVENTORY_ITEM)
        expect(items.first).to_be_visible()
        cart: dict[str, SelectedProduct] = {}

        for i in range(items.count()):
            item: Locator = items.nth(i)
            add_button: Locator = item.locator(PageLocators.ADD_TO_CART)
            add_button_data: str | None = add_button.get_attribute(Values.DATA_TEST)

            if add_button_data is None:
                logger.error(f"{Messages.MISSING_DATA_TEST}, {Values.INDEX}={i}")
                raise RuntimeError

            product_id: str = get_product_slug(add_button_data)
            product = SelectedProduct(
                product_id=product_id,
                name=item.locator(
                    PageLocators.INVENTORY_ITEM_NAME
                ).inner_text().strip(),
                description=item.locator(
                    PageLocators.INVENTORY_ITEM_DESCRIPTION
                ).inner_text().strip(),
                price=handle_str_to_decimal(item.locator(
                    PageLocators.INVENTORY_ITEM_PRICE
                ).inner_text()),
            )
            add_button.click()
            cart[product_id] = product

        badge: Locator = self._page.locator(PageLocators.SHOPPING_CART_BADGE)
        local_cart_len: str = str(len(cart))
        expect(badge).to_have_text(local_cart_len)

        return cart