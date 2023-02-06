from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class CityDetailViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_city_detail(self):
        city = self.cities_create()
        airport = self.airport_create(city)
        response = self.supervisor.get(reverse('city_detail', kwargs={'pk': city.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn(city.name, str(response.content))
        self.assertIn(airport.name, str(response.content))
        self.assertIn(airport.address, str(response.content))
