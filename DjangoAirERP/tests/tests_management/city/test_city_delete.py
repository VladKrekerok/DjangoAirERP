from django.test import TestCase
from django.urls import reverse
from management.models import City
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class CityDeleteViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_city_delete(self):
        city = self.cities_create()
        response = self.supervisor.post(reverse('city_delete', kwargs={'pk': city.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/cities/list')
        self.assertFalse(City.objects.filter(id=city.id).exists())
