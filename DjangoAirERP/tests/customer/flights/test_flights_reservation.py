from django.test import TestCase
from django.urls import reverse
from management.models import Ticket
from mixin_data import DatabaseDataMixin
from mixin_login import AuthClientMixin


class FlightReservationViewTest(AuthClientMixin, DatabaseDataMixin, TestCase):
    def test_get_form_flights_reservation(self):
        flight = self.tickets_create()
        response = self.auth_client.get(reverse('flights_reservation', kwargs={'pk': flight.pk}),
                                        data={'adults': '1',
                                              'children': '0',
                                              'infants': '0',
                                              'class': 'economy'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(flight.from_city.name, str(response.content))
        self.assertIn(flight.to_city.name, str(response.content))
        self.assertIn('Ticket Reservations', str(response.content))
        self.assertIn(f'Price without options {flight.price}$', str(response.content))

    def test_post_flights_reservation(self):
        flight = self.tickets_create()
        response = self.auth_client.post(reverse('flights_reservation', kwargs={'pk': flight.pk}),
                                         data={'adult-TOTAL_FORMS': '1',
                                               'adult-INITIAL_FORMS': '0',
                                               'children-TOTAL_FORMS': '0',
                                               'children-INITIAL_FORMS': '0',
                                               'infants-TOTAL_FORMS': '0',
                                               'infants-INITIAL_FORMS': '0',
                                               'adult-0-first_name': 'test_name',
                                               'adult-0-last_name': 'test_surname',
                                               'adult-0-gender': 'male',
                                               'adult-0-document_no': 'AA344234',
                                               'adult-0-date_birthday': '2000-02-22',
                                               'class': 'economy'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Ticket.objects.filter(first_name='test_name',
                                              last_name='test_surname',
                                              gender='male',
                                              document_no='AA344234',
                                              flight=flight).exists())
