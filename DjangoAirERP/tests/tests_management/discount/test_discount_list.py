from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class DiscountListViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_discount_list(self):
        self.discounts_create(3)
        response = self.supervisor.get(reverse('discount_list'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('promo-code1', str(response.content))
        self.assertIn('promo-code2', str(response.content))
        self.assertIn('promo-code3', str(response.content))
