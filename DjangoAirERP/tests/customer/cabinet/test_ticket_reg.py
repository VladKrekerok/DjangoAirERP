from django.test import TestCase
from django.urls import reverse
from management.models import Ticket
from mixin_data import DatabaseDataMixin
from mixin_login import AuthClientMixin


class TicketRegisterViewTest(AuthClientMixin, DatabaseDataMixin, TestCase):
    def test_ticket_reg(self):
        ticket = self.ticket_holder(self.user)
        discount = self.discounts_create(1)

        response = self.auth_client.post(reverse('ticket_reg', kwargs={'id': self.user.pk, 'pk': ticket.id}),
                                         data={'promo_code': discount.name})

        updated = Ticket.objects.filter(id=ticket.id).first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/cabinet/{self.user.id}/tickets/{ticket.id}')
        self.assertEqual(updated.self_check_in, True)
        self.assertIsNotNone(updated.place)
        self.assertEqual(updated.discount, discount)
        self.assertEqual(updated.price_with_options,
                         ticket.price * (100 - int(discount.percents.replace('%', ''))) / 100)
