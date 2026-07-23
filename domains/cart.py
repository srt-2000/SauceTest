"""Domain value object for a product selected into the cart."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class SelectedProductValueObject:
    """Product added to cart and stored in local cart state.

    Attributes:
        product_id: Product slug (e.g. from ``data-test`` without prefix).
        name: Display name on the inventory / cart page.
        description: Product description text.
        price: Unit price as ``Decimal``.
    """

    product_id: str
    name: str
    description: str
    price: Decimal
