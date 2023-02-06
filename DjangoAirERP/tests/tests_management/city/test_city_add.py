from django.test import TestCase
from django.urls import reverse
from management.models import City
from mixin_login import SupervisorMixin


class CityCreateViewTest(SupervisorMixin, TestCase):
    def test_city_create(self):
        response = self.supervisor.post(reverse('city_add'), data={'name': 'Kharkov',
                                                                   'country': 'UA'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/cities/list')
        self.assertTrue(City.objects.filter(name='Kharkov',
                                            country='UA').exists())
