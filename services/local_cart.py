"""In-memory cart state for the SauceDemo purchase flow."""

from __future__ import annotations

from loguru import logger

from domains import SelectedProduct
from services.constants import Messages


class LocalCart:
    """Local cart keyed by product slug; insertion order is preserved.

    Attributes:
        _items: Internal mapping of product slug to ``SelectedProduct``.
    """

    def __init__(self) -> None:
        """Create an empty local cart."""
        self._items: dict[str, SelectedProduct] = {}

    def add(self, product_to_add: SelectedProduct) -> None:
        """Add or replace a product in the local cart.

        Args:
            product_to_add: Product to store under its ``product_id`` key.
        """
        item_id: str = product_to_add.product_id
        self._items[item_id] = product_to_add

    def pop_last(self) -> SelectedProduct:
        """Remove and return the rightmost (last inserted) product.

        Corresponds to scenario step 4.

        Returns:
            The removed ``SelectedProduct``.

        Raises:
            KeyError: If the cart is empty.
        """
        if not self._items:
            logger.error(Messages.EMPTY_CART)
            raise KeyError(Messages.EMPTY_CART)

        product_id, product = self._items.popitem()
        logger.info(f"{Messages.POP_LAST_FROM_CART}: {product_id}")

        return product

    def remove(self, product_id: str) -> SelectedProduct:
        """Remove a product by slug from the local cart.

        Args:
            product_id: Product slug to remove.

        Returns:
            The removed ``SelectedProduct``.

        Raises:
            KeyError: If ``product_id`` is not in the cart.
        """
        if product_id not in self._items:
            logger.error(f"{Messages.PRODUCT_ID_NOT_IN_CART}: {product_id}")
            raise KeyError(product_id)

        return self._items.pop(product_id)

    @property
    def get_items(self) -> dict[str, SelectedProduct]:
        """Return a shallow copy of the cart mapping.

        Returns:
            Copy of slug → product mapping (insertion order preserved).
        """
        return dict(self._items)

    def __len__(self) -> int:
        """Return the number of products in the local cart.

        Returns:
            Item count.
        """
        return len(self._items)

    def __contains__(self, product_id: str) -> bool:
        """Return whether ``product_id`` is in the local cart.

        Args:
            product_id: Product slug to check.

        Returns:
            ``True`` if the slug is present, otherwise ``False``.
        """
        return product_id in self._items
