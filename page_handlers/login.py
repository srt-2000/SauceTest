"""Login page actions for SauceDemo."""
from playwright.sync_api import Page, expect
from page_handlers.constants import PageLocators


class LoginPage:
    """Interact with the SauceDemo login form."""

    def __init__(self, page: Page) -> None:
        """Bind Playwright page instance."""
        self._page = page

    def login(self, username: str, password: str) -> None:
        """Authenticate and wait for the inventory list."""
        self._page.locator(PageLocators.USERNAME).fill(username)
        self._page.locator(PageLocators.PASSWORD).fill(password)
        self._page.locator(PageLocators.LOGIN_BUTTON).click()
        expect(self._page.locator(PageLocators.INVENTORY_LIST)).to_be_visible()
