"""SauceDemo end-to-end purchase scenario entry point."""

from playwright.sync_api import sync_playwright, Browser, Page
from loguru import logger
from pathlib import Path

from config import settings
from constants import DOM_CONTENT_LOADED, Values, Messages
from domains.cart import SelectedProductValueObject
from domains.order import OrderSummaryDTO
from page_handlers.cart import CartPage
from page_handlers.inventory import InventoryPage
from page_handlers.login import LoginPage
from services.local_cart import LocalCart
from page_handlers.checkout import CheckoutPage
from services.order_xlsx import OrderXLSXExporter

RESULT_DIR = Path(__file__).resolve().parent / "result"


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
        removed_product: SelectedProductValueObject = local_cart.pop_last()
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

        # 8
        checkout = CheckoutPage(new_page)
        checkout.fill_form(
            settings.USER_FIRST_NAME,
            settings.USER_LAST_NAME,
            settings.ZIP_CODE,
        )
        checkout.send_filled_form()
        logger.info(Messages.USER_INFO_FORM_SENT)

        # 9
        order: OrderSummaryDTO = checkout.get_order_summary(local_cart)
        xlsx_writer = OrderXLSXExporter()
        xlsx_path = xlsx_writer.export_order_summary_to_xlsx(
            order,
            RESULT_DIR / Values.XLSX_FILE_NAME,
        )
        logger.info(f"{Messages.XLSX_SAVED}: {xlsx_path}")
        checkout.finish()

        # 10
        pdf_path = checkout.download_pdf(RESULT_DIR / Values.PDF_FILE_NAME)
        logger.info(f"{Messages.PDF_SAVED}: {pdf_path}")

        browser.close()


if __name__ == "__main__":
    run()
