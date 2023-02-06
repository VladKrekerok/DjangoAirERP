from django.test import TestCase
from django.urls import reverse
from management.models import Airplane
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class AirplaneDeleteViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_airplane_delete(self):
        airplane = self.airplane_create()
        response = self.supervisor.post(reverse('airplane_delete', kwargs={'pk': airplane.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/airplane/list')
        self.assertFalse(Airplane.objects.filter(id=airplane.id).exists())
