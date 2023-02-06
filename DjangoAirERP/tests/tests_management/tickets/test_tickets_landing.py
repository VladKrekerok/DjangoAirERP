from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from management.models import Ticket
from mixin_data import DatabaseDataMixin
from mixin_login import GateManagerMixin


class GateManagerViewTest(GateManagerMixin, DatabaseDataMixin, TestCase):
    def test_tickets_landing(self):
        ticket = self.ticket_register()
        ticket.check_in = True
        ticket.save()
        ticket.flight.departure_date = (datetime.now() + timedelta(minutes=55)).strftime("%Y-%m-%dT%H:%M")
        ticket.flight.save()

        response = self.gate.post(reverse('tickets_landing', kwargs={'pk': ticket.id}))

        self.assertEqual(response.status_code, 200)
        updated = Ticket.objects.filter(id=ticket.id).first()
        self.assertIsNotNone(updated.boarding_time)
        self.assertTrue(updated.boarding)
