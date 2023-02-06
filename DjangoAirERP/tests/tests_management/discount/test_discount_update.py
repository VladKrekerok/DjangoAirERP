from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from management.models import Discount
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class DiscountUpdateViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_discount_update(self):
        discount = self.discounts_create(1)
        response = self.supervisor.post(reverse('discount_update', kwargs={'pk': discount.id}),
                                        data={'name': 'new-promo',
                                              'percents': '90%',
                                              'valid_until': datetime.today().date()})

        updated = Discount.objects.filter(id=discount.id).first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/discount/list')
        self.assertEqual(updated.name, 'new-promo')
        self.assertEqual(updated.percents, '90%')
