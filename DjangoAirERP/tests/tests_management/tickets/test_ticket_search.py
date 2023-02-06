from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class TicketSearchViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_ticket_search(self):
        ticket = self.ticket_register()
        response = self.supervisor.get(reverse('search_ticket'), data={'code': ticket.id})

        self.assertEqual(response.status_code, 200)
        self.assertIn(ticket.flight.from_city.name, str(response.content))
        self.assertIn(ticket.flight.to_city.name, str(response.content))
        self.assertIn(ticket.first_name, str(response.content))
        self.assertIn(ticket.last_name, str(response.content))
        self.assertIn(ticket.years_old, str(response.content))
        self.assertIn(str(ticket.place), str(response.content))
        self.assertIn(str(ticket.price), str(response.content))
        self.assertIn(ticket.place_type, str(response.content))
