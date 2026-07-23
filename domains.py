"""Domain models for cart products and order confirmation."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class SelectedProduct:
    """Product added to cart and stored in local cart state.

    Attributes:
        product_id: Product slug derived from the add-to-cart ``data-test``.
        name: Display name from the inventory card.
        description: Product description text.
        price: Unit price as ``Decimal``.
    """

    product_id: str
    name: str
    description: str
    price: Decimal


@dataclass(slots=True)
class OrderSummary:
    """Order confirmation fields for later XLSX export.

    Attributes:
        payment_info: Payment method text from the confirmation page.
        shipping_info: Shipping method text from the confirmation page.
        tax: Tax amount.
        total: Order total including tax.
        items: Mapping of product slug to ``SelectedProduct``.
    """

    payment_info: str
    shipping_info: str
    tax: Decimal
    total: Decimal
    items: dict[str, SelectedProduct]
