"""Domain Data Transfer Objects for order confirmation."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class OrderLineDTO:
    """Checkout overview line for XLSX export (qty from step-two only).

    Attributes:
        product_id: Product slug matching local cart.
        name: Display name scraped from overview.
        description: Product description from local cart.
        price: Unit price as ``Decimal``.
        qty: Quantity from the checkout step-two DOM.
    """

    product_id: str
    name: str
    description: str
    price: Decimal
    qty: int


@dataclass(slots=True)
class OrderSummaryDTO:
    """Order confirmation payload for XLSX export.

    Attributes:
        payment_info: Payment method text from overview.
        shipping_info: Shipping method text from overview.
        ship_to: Buyer ship-to string (name + ZIP).
        items_total: Subtotal before tax.
        tax: Tax amount.
        total: Grand total including tax.
        lines: Ordered line items for the report.
    """

    payment_info: str
    shipping_info: str
    ship_to: str
    items_total: Decimal
    tax: Decimal
    total: Decimal
    lines: tuple[OrderLineDTO, ...]
