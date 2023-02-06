from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import AuthClientMixin


class TicketDetailViewTest(AuthClientMixin, DatabaseDataMixin, TestCase):
    def test_ticket_detail(self):
        ticket = self.ticket_holder(self.user)

        response = self.auth_client.get(reverse('ticket_detail', kwargs={'id': self.user.pk, 'pk': ticket.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn(ticket.flight.from_city.name, str(response.content))
        self.assertIn(ticket.flight.to_city.name, str(response.content))
        self.assertIn(ticket.flight.from_airport.name, str(response.content))
        self.assertIn(ticket.flight.to_airport.name, str(response.content))
        self.assertIn(str(ticket.id), str(response.content))
        self.assertIn(ticket.first_name, str(response.content))
        self.assertIn(ticket.last_name, str(response.content))
        self.assertIn(ticket.place_type, str(response.content))
        self.assertIn(str(ticket.price), str(response.content))
