from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import AuthClientMixin


class TicketListViewTest(AuthClientMixin, DatabaseDataMixin, TestCase):
    def test_customer_tickets(self):
        ticket = self.ticket_holder(self.user)

        response = self.auth_client.get(reverse('customer_tickets', kwargs={'pk': self.user.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertIn(ticket.flight.from_city.name, str(response.content))
        self.assertIn(ticket.flight.to_city.name, str(response.content))
