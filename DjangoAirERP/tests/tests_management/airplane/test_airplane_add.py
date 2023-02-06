from django.test import TestCase
from django.urls import reverse
from management.models import Airplane
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class AirplaneCreateViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_airplane_add(self):
        city = self.cities_create()
        response = self.supervisor.post(reverse('airplane_add'), data={'location': city.id,
                                                                       'model': 'ModelTest',
                                                                       'name': 'AirplaneTest',
                                                                       'comfort_places': 5,
                                                                       'economy_places': 5})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/management/airplane/list')
        self.assertTrue(Airplane.objects.filter(location=city,
                                                name='AirplaneTest',
                                                model='ModelTest',
                                                comfort_places=5,
                                                economy_places=5).exists())
