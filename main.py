"""SauceDemo end-to-end purchase scenario entry point."""

from playwright.sync_api import sync_playwright, Browser, Page
from loguru import logger

from config import settings
from constants import DOM_CONTENT_LOADED, Values, Messages
from domains import SelectedProduct
from page_handlers.cart import CartPage
from page_handlers.inventory import InventoryPage
from page_handlers.login import LoginPage
from services.local_cart import LocalCart


def run() -> None:
    """Execute the full SauceDemo purchase scenario.

    Opens Chromium, logs in, adds all inventory products to a local cart,
    removes the last item from local and site carts, asserts sync, then
    starts checkout.
    """
    with sync_playwright() as p:
        # 0
        p.selectors.set_test_id_attribute(Values.DATA_TEST)
        browser: Browser = p.chromium.launch(headless=False)
        new_page: Page = browser.new_page()
        new_page.goto(
            settings.RESOURCE_URL,
            wait_until=DOM_CONTENT_LOADED,
        )
        logger.info(f"{Messages.PREPARE_FOR_LOGIN}: {new_page.url}")
        # 1
        LoginPage(new_page).login(settings.STANDARD_USER, settings.PASSWORD)
        logger.info(Messages.LOGGED)
        # 2 and 3
        local_cart: LocalCart = InventoryPage(
            new_page
        ).add_all_products_to_cart_and_collect_cart_locally()
        local_cart_for_log: list[str] = list(local_cart.get_items)
        logger.info(f"{Messages.ADDED_ITEMS}: {local_cart_for_log}")
        # 4
        removed_product: SelectedProduct = local_cart.pop_last()
        removed_slug: str = removed_product.product_id
        logger.info(f"{Messages.POP_ITEM_FROM_CART}: {removed_slug}")
        # 5
        cart_page = CartPage(new_page)
        cart_page.open()
        logger.info(Messages.OPENED_CART)
        # 6
        cart_page.remove_product(removed_slug)
        logger.info(f"{Messages.REMOVED_PRODUCT_ON_WEB}: {removed_slug}")
        # 7
        cart_page.assert_matches_local_and_web(local_cart)
        logger.info(Messages.CHECKED_CARTS_SYNC)
        cart_page.checkout()
        logger.info(Messages.CHECKOUT)

        # 7-8 checkout + form
        # 9 scrape payment/shipping/tax, Finish
        # 10 expect_download -> PDF
        # 11 xlsx later
        browser.close()


if __name__ == "__main__":
    run()
