"""Cart page: open, remove on site, assert sync, checkout."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from domains import SelectedProduct
from page_handlers.constants import PageLocators, Values
from services.local_cart import LocalCart


class CartPage:
    """Cart page interactions for scenario steps 5–7."""

    def __init__(self, page: Page) -> None:
        """Bind a Playwright page instance.

        Args:
            page: Active Playwright ``Page``.
        """
        self._page = page

    def open(self) -> None:
        """Open the cart page (step 5)."""
        self._page.locator(PageLocators.SHOPPING_CART_LINK).click()
        expect(self._page.locator(PageLocators.CART_ITEM).first).to_be_visible()

    def remove_product(self, product_id: str) -> None:
        """Remove one product from the site cart by slug (step 6).

        Args:
            product_id: Product slug matching the remove button ``data-test``.
        """
        remove_id_prefix: str = f"{Values.REMOVE_PREFIX}{product_id}"

        self._page.get_by_test_id(remove_id_prefix).click()
        expect(self._page.get_by_test_id(remove_id_prefix)).to_have_count(0)

    def assert_matches_local_and_web(self, local_cart: LocalCart) -> None:
        """Assert site cart size and items match the local cart (step 7).

        Args:
            local_cart: In-memory cart expected to match the site.
        """
        local_cart_len: int = len(local_cart)
        expect(self._page.locator(PageLocators.CART_ITEM)).to_have_count(local_cart_len)

        if len(local_cart):
            local_cart_len_text: str = str(local_cart_len)
            expect(self._page.locator(PageLocators.SHOPPING_CART_BADGE)).to_have_text(
                local_cart_len_text
            )

        local_cart_products: dict[str, SelectedProduct] = local_cart.get_items
        for product_id in local_cart_products:
            expect(
                self._page.get_by_test_id(f"{Values.REMOVE_PREFIX}{product_id}")
            ).to_be_visible()

    def checkout(self) -> None:
        """Confirm selection and start checkout (end of step 7)."""
        self._page.locator(PageLocators.CHECKOUT_BUTTON).click()
        expect(self._page.locator(PageLocators.CHECKOUT_INFO)).to_be_visible()
