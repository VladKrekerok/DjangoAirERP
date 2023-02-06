from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class FlightsListViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_flights_list(self):
        self.flights_create()

        response = self.supervisor.get(reverse('flights_list'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('UA Kharkov airport-Kharkov', str(response.content))
        self.assertIn('UA Kiev airport-Kiev', str(response.content))
        self.assertIn('Airplane-1 model1', str(response.content))
        self.assertIn('Airplane-2 model2', str(response.content))
        self.assertIn('3h 0min', str(response.content))
