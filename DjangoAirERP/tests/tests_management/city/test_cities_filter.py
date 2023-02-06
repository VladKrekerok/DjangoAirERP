from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class CitiesFilterViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_cities_filter(self):
        city = self.cities_create()
        response = self.supervisor.get(reverse('cities_filter'), data={'name': city.name,
                                                                       'country': city.country})

        self.assertEqual(response.status_code, 200)
        self.assertIn(city.name, str(response.content))
        self.assertIn(city.country, str(response.content))
