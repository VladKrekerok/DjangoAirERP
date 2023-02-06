from django.test import TestCase
from django.urls import reverse
from management.models import Flight
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class FlightDeleteViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_flight_delete(self):
        flight = self.flights_create()
        response = self.supervisor.post(reverse('flight_delete', kwargs={'pk': flight.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/flights/list')
        self.assertFalse(Flight.objects.filter(id=flight.id).exists())
