from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from management.models import Discount
from mixin_login import SupervisorMixin


class DiscountCreateViewTest(SupervisorMixin, TestCase):
    def test_discount_add(self):
        response = self.supervisor.post(reverse('discount_add'), data={'name': 'promo-code',
                                                                       'percents': '50%',
                                                                       'valid_until': datetime.today().date()})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/discount/list')
        self.assertTrue(Discount.objects.filter(name='promo-code',
                                                percents='50%',
                                                valid_until=datetime.today().date()).exists())
