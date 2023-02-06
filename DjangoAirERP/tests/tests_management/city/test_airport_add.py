from django.test import TestCase
from django.urls import reverse
from management.models import Airport
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class AirportCreateViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_airport_add(self):
        city = self.cities_create()
        response = self.supervisor.post(reverse('airport_add', kwargs={'pk': city.id}), data={'name': 'new-airport',
                                                                                              'address': 'airport 19'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/management/cities/{city.id}/detail')
        self.assertTrue(Airport.objects.filter(city=city, name='new-airport', address='airport 19').exists())
