from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import GroceryOrder, GroceryStore, OrderEvent, OutboxEvent, Product
from .services import create_grocery_order


class TransactionalOrderingTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(username='owner', password='test-pass-123')
        self.customer = User.objects.create_user(username='customer', password='test-pass-123')
        self.store = GroceryStore.objects.create(
            owner=self.owner, name='Test Store', phone='1234567890',
            address='Test address', store_type='veg'
        )
        self.product = Product.objects.create(
            grocery_store=self.store, name='Rice', price='50.00', stock=5
        )

    def test_order_decrements_stock_and_calculates_total(self):
        order = create_grocery_order(
            customer=self.customer, store=self.store, quantities={self.product.id: 3}
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 2)
        self.assertEqual(order.total_price, 150)
        self.assertEqual(order.groceryorderitem_set.get().quantity, 3)

    def test_insufficient_stock_rolls_back_entire_order(self):
        with self.assertRaisesMessage(ValidationError, 'Insufficient stock'):
            create_grocery_order(
                customer=self.customer, store=self.store, quantities={self.product.id: 6}
            )
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)
        self.assertFalse(GroceryOrder.objects.exists())

    def test_idempotent_retry_does_not_charge_stock_twice(self):
        first = create_grocery_order(
            customer=self.customer, store=self.store,
            quantities={self.product.id: 2}, idempotency_key='request-123',
        )
        second = create_grocery_order(
            customer=self.customer, store=self.store,
            quantities={self.product.id: 2}, idempotency_key='request-123',
        )
        self.product.refresh_from_db()
        self.assertEqual(first.id, second.id)
        self.assertEqual(self.product.stock, 3)
        self.assertEqual(OrderEvent.objects.count(), 1)
        self.assertEqual(OutboxEvent.objects.count(), 1)
