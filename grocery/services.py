"""Transactional ordering services that keep stock and orders consistent."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import GroceryOrder, GroceryOrderItem, GroceryStore, OrderEvent, OutboxEvent, Product


@transaction.atomic
def create_grocery_order(
    *, customer, store: GroceryStore, quantities: dict[int, int], idempotency_key: str | None = None
) -> GroceryOrder:
    """Create an order and reserve stock atomically.

    Product rows are locked until the transaction commits, preventing two
    simultaneous orders from overselling the same inventory.
    """
    if idempotency_key:
        existing = GroceryOrder.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            if existing.customer_id != customer.id or existing.store_id != store.id:
                raise ValidationError('The idempotency key belongs to another order context.')
            return existing

    requested = {int(pid): int(qty) for pid, qty in quantities.items() if int(qty) > 0}
    if not requested:
        raise ValidationError('At least one positive item quantity is required.')

    products = {
        product.id: product
        for product in Product.objects.select_for_update().filter(
            id__in=requested, grocery_store=store
        )
    }
    if set(products) != set(requested):
        raise ValidationError('One or more products do not belong to this store.')

    for product_id, quantity in requested.items():
        if products[product_id].stock < quantity:
            raise ValidationError(
                f'Insufficient stock for {products[product_id].name}: '
                f'requested {quantity}, available {products[product_id].stock}.'
            )

    order = GroceryOrder.objects.create(
        customer=customer, store=store, idempotency_key=idempotency_key
    )
    total = Decimal('0')
    order_items = []
    changed_products = []
    for product_id, quantity in requested.items():
        product = products[product_id]
        line_total = product.price * quantity
        total += line_total
        product.stock -= quantity
        changed_products.append(product)
        order_items.append(GroceryOrderItem(
            order=order, product=product, quantity=quantity, price=line_total
        ))

    Product.objects.bulk_update(changed_products, ['stock'])
    GroceryOrderItem.objects.bulk_create(order_items)
    order.total_price = total
    order.save(update_fields=['total_price'])
    event_payload = {'order_id': order.id, 'store_id': store.id, 'total': str(total)}
    OrderEvent.objects.create(order=order, event_type='order.placed', payload=event_payload)
    OutboxEvent.objects.create(topic='order.placed', payload=event_payload)
    return order
