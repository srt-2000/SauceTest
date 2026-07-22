from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Product:
    """Product captured from the storefront."""
    name: str
    description: str
    price: float
    remove_id: str | None = None


@dataclass(slots=True)
class OrderSummary:
    """Order confirmation fields for later XLSX export."""

    payment_info: str
    shipping_info: str
    tax: float
    total: float
    items: list[Product]
