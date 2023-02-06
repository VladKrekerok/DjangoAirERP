from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class CitiesListViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_city_list(self):
        self.cities_create()
        response = self.supervisor.get(reverse('cities_list'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Kharkov', str(response.content))
        self.assertIn('Kherson', str(response.content))
        self.assertIn('Kiev', str(response.content))
