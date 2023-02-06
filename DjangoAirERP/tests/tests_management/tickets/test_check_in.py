from django.test import TestCase
from django.urls import reverse
from management.models import Ticket
from mixin_data import DatabaseDataMixin
from mixin_login import CheckInManagerMixin


class CheckInManagerViewTest(CheckInManagerMixin, DatabaseDataMixin, TestCase):
    def test_check_in(self):
        ticket = self.ticket_register()
        response = self.check_in.post(reverse('check_in', kwargs={'pk': ticket.id}), data={'luggage_weight': 10})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/tickets/search')
        updated = Ticket.objects.filter(id=ticket.id).first()
        self.assertEqual(updated.luggage_weight, 10)
        self.assertEqual(updated.check_in, True)
        self.assertEqual(updated.payment_status, True)
