from playwright.sync_api import sync_playwright, Browser, Page

from config import settings
from constants import DOM_CONTENT_LOADED
from domains import SelectedProduct
from page_handlers.inventory import InventoryPage
from page_handlers.login import LoginPage


def run() -> None:
    """Execute the full SauceDemo purchase scenario."""
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        new_page: Page = browser.new_page()
        new_page.goto(
            settings.RESOURCE_URL,
            wait_until=DOM_CONTENT_LOADED,
        )

        LoginPage(new_page).login(settings.STANDARD_USER, settings.PASSWORD)
        cart: dict[str, SelectedProduct] = InventoryPage(new_page).add_all_products_to_cart_and_collect_cart_locally()
        print(cart)

        # 1 login
        # 2 add N items
        # 3 scrape -> list[Product]
        # 4 pop один локально
        # 5 cart
        # 6 sync UI с list[Product]
        # 7-8 checkout + form
        # 9 scrape payment/shipping/tax, Finish
        # 10 expect_download -> PDF
        # 11 xlsx later
        browser.close()

if __name__ == "__main__":
    run()
