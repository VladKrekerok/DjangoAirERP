from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class FlightDetailViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_flight_detail(self):
        flight = self.flights_create()
        response = self.supervisor.get(reverse('flight_detail', kwargs={'pk': flight.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn(flight.from_city.name, str(response.content))
        self.assertIn(flight.to_city.name, str(response.content))
        self.assertIn(flight.airplane.name, str(response.content))
        self.assertIn(flight.from_airport.name, str(response.content))
        self.assertIn(flight.to_airport.name, str(response.content))
        self.assertIn(str(flight.airplane.comfort_places), str(response.content))
        self.assertIn(str(flight.airplane.economy_places), str(response.content))
