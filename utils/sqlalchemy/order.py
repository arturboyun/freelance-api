from typing import Callable

from sqlalchemy import desc, asc


def get_order_direction(direction: str) -> Callable:
    """Return desc or asc function based on direction."""
    return desc if direction == "desc" else asc
