from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import AuthClientMixin


class TicketSearchViewTest(AuthClientMixin, DatabaseDataMixin, TestCase):
    def test_ticket_search(self):
        ticket = self.ticket_holder(self.user)

        response = self.auth_client.get(reverse('ticket_search', kwargs={'id': self.user.pk}),
                                        data={'code': ticket.id}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Register a ticket", str(response.content))
        self.assertIn("Promo code for a discount", str(response.content))
        self.assertIn("- The ticket will become registered to you.", str(response.content))
        self.assertIn("- Your place will be indicated on the ticket.", str(response.content))
