from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class FlightsFilterViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_flights_filter(self):
        flight = self.flights_create()
        response = self.supervisor.get(reverse('flights_filter'), data={'from_city': flight.from_city.name,
                                                                        'to_city': flight.to_city.name})

        self.assertEqual(response.status_code, 200)
        self.assertIn(flight.from_city.name, str(response.content))
        self.assertIn(flight.to_city.name, str(response.content))
        self.assertIn(flight.airplane.name, str(response.content))
        self.assertIn(flight.from_airport.name, str(response.content))
        self.assertIn(flight.to_airport.name, str(response.content))
