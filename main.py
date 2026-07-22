from playwright.sync_api import sync_playwright

from config import settings


def run() -> None:
    """Execute the full SauceDemo purchase scenario."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # сначала False, отладка
        page = browser.new_page()
        page.goto(settings.RESOURCE_URL)
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
