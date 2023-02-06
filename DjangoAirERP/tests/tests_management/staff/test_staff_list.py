from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class StaffCreateViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_staff_list(self):
        self.staff_create()
        response = self.supervisor.get(reverse('staff_list'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('gate', str(response.content))
        self.assertIn('check-in', str(response.content))
        self.assertIn('supervisor', str(response.content))
