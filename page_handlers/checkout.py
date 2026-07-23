"""Checkout info, overview scrape, finish, and PDF download."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from loguru import logger
from playwright.sync_api import Page, expect, Download

from config import settings
from domains.order import OrderSummaryDTO, OrderLineDTO
from domains.cart import SelectedProductValueObject
from page_handlers.constants import PageLocators, Messages
from page_handlers.utils import to_clear_labeled_price_to_decimal_digit
from services.local_cart import LocalCart


class CheckoutPage:
    """Checkout steps 8–10 for SauceDemo."""

    def __init__(self, page: Page) -> None:
        """Bind a Playwright page instance.

        Args:
            page: Active Playwright ``Page``.
        """
        self._page = page

    def fill_form(
        self,
        first_name: str,
        last_name: str,
        zip_code: str,
    ) -> None:
        """Fill checkout info fields (step 8, before Continue).

        Args:
            first_name: Buyer first name.
            last_name: Buyer last name.
            zip_code: Postal / ZIP code.
        """
        self._page.locator(PageLocators.FIRST_NAME).fill(first_name)
        self._page.locator(PageLocators.LAST_NAME).fill(last_name)
        self._page.locator(PageLocators.POSTAL_CODE).fill(zip_code)

        return

    def send_filled_form(self) -> None:
        """Submit checkout info and wait for the overview summary."""
        self._page.locator(PageLocators.CONTINUE_BUTTON).click()
        expect(self._page.locator(PageLocators.SUMMARY_INFO)).to_be_visible()

        return

    def _build_order_lines(self, local_cart: LocalCart) -> tuple[OrderLineDTO, ...]:
        """Build ``OrderLineDTO`` rows from local cart data and DOM qty.

        Args:
            local_cart: In-memory cart used for name/price/description.

        Returns:
            Tuple of overview lines in DOM order.

        Raises:
            KeyError: If an overview product name is missing from ``local_cart``.
        """
        by_name: dict[str, SelectedProductValueObject] = {
            product.name: product for product in local_cart.get_items.values()
        }
        lines: list[OrderLineDTO] = []
        rows = self._page.locator(PageLocators.CART_ITEM)

        for i in range(rows.count()):
            row = rows.nth(i)
            name = row.locator(PageLocators.INVENTORY_ITEM_NAME).inner_text().strip()
            qty = int(row.locator(PageLocators.CART_QUANTITY).inner_text().strip())

            product = by_name.get(name)
            if product is None:
                logger.error("{}: {!r}", Messages.PRODUCT_NOT_IN_LOCAL_CART, name)
                raise KeyError(name)

            lines.append(
                OrderLineDTO(
                    product_id=product.product_id,
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    qty=qty,
                )
            )

        return tuple(lines)

    def get_order_summary(self, local_cart: LocalCart) -> OrderSummaryDTO:
        """Scrape checkout overview into ``OrderSummaryDTO`` (step 9).

        Args:
            local_cart: Local cart for line item enrichment.

        Returns:
            Order summary with payment, shipping, totals, and lines.
        """
        payment_info: str = self._page.locator(
            PageLocators.PAYMENT_INFO_VALUE
        ).inner_text().strip()

        shipping_info: str = self._page.locator(
            PageLocators.SHIPPING_INFO_VALUE
        ).inner_text().strip()

        ship_to: str = (
            f"{settings.USER_FIRST_NAME}, {settings.USER_LAST_NAME}, "
            f"{settings.ZIP_CODE}"
        )

        items_total: Decimal = to_clear_labeled_price_to_decimal_digit(
            self._page.locator(PageLocators.ITEM_TOTAL_LABEL).inner_text()
        )

        tax: Decimal = to_clear_labeled_price_to_decimal_digit(
            self._page.locator(PageLocators.TAX_LABEL).inner_text()
        )

        total: Decimal = to_clear_labeled_price_to_decimal_digit(
            self._page.locator(PageLocators.TOTAL_LABEL).inner_text()
        )

        lines: tuple[OrderLineDTO, ...] = self._build_order_lines(local_cart)

        order_summary: OrderSummaryDTO = OrderSummaryDTO(
            payment_info=payment_info,
            shipping_info=shipping_info,
            ship_to=ship_to,
            items_total=items_total,
            tax=tax,
            total=total,
            lines=lines,
        )

        return order_summary

    def finish(self) -> None:
        """Click Finish and wait for the complete page header."""
        self._page.locator(PageLocators.FINISH_BUTTON).click()
        expect(self._page.locator(PageLocators.COMPLETE_HEADER)).to_be_visible()

        return

    def download_pdf(self, target_path: Path) -> Path:
        """Download the generated order PDF (step 10).

        Args:
            target_path: Destination path for the saved PDF file.

        Returns:
            The same ``target_path`` after download.
        """
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with self._page.expect_download() as download_info:
            self._page.locator(PageLocators.GENERATE_PDF_BUTTON).click()
        download: Download = download_info.value
        download.save_as(target_path)

        return target_path
