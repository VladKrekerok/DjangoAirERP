from django.test import TestCase
from django.urls import reverse
from management.models import Airplane, City
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class AirplaneUpdateViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_airplane_update(self):
        airplane = self.airplane_create()
        city = City.objects.filter(name='Kharkov').first()

        response = self.supervisor.post(reverse('airplane_update', kwargs={'pk': airplane.id}),
                                        data={'location': city.id,
                                              'model': 'new-model',
                                              'name': 'NewName',
                                              'comfort_places': 7,
                                              'economy_places': 8})

        updated = Airplane.objects.filter(id=airplane.id).first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/airplane/list')

        self.assertEqual(updated.location, city)
        self.assertEqual(updated.model, 'new-model')
        self.assertEqual(updated.name, 'NewName')
        self.assertEqual(updated.comfort_places, 7)
        self.assertEqual(updated.economy_places, 8)
