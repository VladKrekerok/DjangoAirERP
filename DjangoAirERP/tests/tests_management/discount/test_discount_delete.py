from django.test import TestCase
from django.urls import reverse
from management.models import Discount
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class DiscountDeleteViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_discount_delete(self):
        discount = self.discounts_create(1)
        response = self.supervisor.post(reverse('discount_delete', kwargs={'pk': discount.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/discount/list')
        self.assertFalse(Discount.objects.filter(id=discount.id).exists())
