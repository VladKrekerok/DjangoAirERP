from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class AirplaneListViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_airplane_list(self):
        self.airplane_create()
        response = self.supervisor.get(reverse('airplane_list'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Airplane-0', str(response.content))
        self.assertIn('Airplane-1', str(response.content))
        self.assertIn('Airplane-2', str(response.content))
