"""Deterministic delivery assignment baselines."""

from dataclasses import dataclass
from math import hypot


@dataclass(frozen=True)
class Courier:
    courier_id: int
    x: float
    y: float
    active_orders: int = 0


def assign_nearest_balanced(
    order_location: tuple[float, float], couriers: list[Courier], load_penalty: float = 1.0
) -> Courier:
    """Minimize Euclidean distance plus a transparent workload penalty."""
    if not couriers or load_penalty < 0:
        raise ValueError('At least one courier and a non-negative penalty are required.')
    x, y = order_location
    return min(
        couriers,
        key=lambda courier: (
            hypot(courier.x - x, courier.y - y) + load_penalty * courier.active_orders,
            courier.courier_id,
        ),
    )
