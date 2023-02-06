from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import AuthClientMixin


class FlightViewTest(AuthClientMixin, DatabaseDataMixin, TestCase):
    def test_flights_search(self):
        flight = self.tickets_create()
        response = self.auth_client.get(reverse('flights_search'), data={'from_city': flight.from_city.name,
                                                                         'to_city': flight.to_city.name,
                                                                         'date': flight.departure_date.date(),
                                                                         'adults': '1',
                                                                         'children': '0',
                                                                         'infants': '0',
                                                                         'class': 'economy'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(flight.flight_time, str(response.content))
        self.assertIn(flight.from_city.name, str(response.content))
        self.assertIn(flight.to_city.name, str(response.content))
        self.assertIn(flight.from_airport.name, str(response.content))
        self.assertIn(flight.to_airport.name, str(response.content))
        self.assertIn(str(flight.departure_date.time().strftime('%H:%M')), str(response.content))
        self.assertIn(str(flight.date_arrival.time().strftime('%H:%M')), str(response.content))
        self.assertIn(str(flight.airplane.economy_places), str(response.content))
