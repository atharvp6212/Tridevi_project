from django.test import SimpleTestCase

from .routing import Courier, assign_nearest_balanced


class CourierAssignmentTests(SimpleTestCase):
    def test_balances_distance_and_workload(self):
        couriers = [Courier(1, 0, 0, 10), Courier(2, 2, 0, 0)]
        self.assertEqual(assign_nearest_balanced((0, 0), couriers).courier_id, 2)

    def test_rejects_empty_pool(self):
        with self.assertRaises(ValueError):
            assign_nearest_balanced((0, 0), [])
