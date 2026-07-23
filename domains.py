from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class SelectedProduct:
    """Product added to cart and stored in local cart state."""
    product_id: str
    name: str
    description: str
    price: Decimal


@dataclass(slots=True)
class OrderSummary:
    """Order confirmation fields for later XLSX export."""

    payment_info: str
    shipping_info: str
    tax: Decimal
    total: Decimal
    items: dict[str, SelectedProduct]
