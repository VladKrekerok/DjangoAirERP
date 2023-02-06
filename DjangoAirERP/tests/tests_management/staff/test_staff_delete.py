from django.test import TestCase
from django.urls import reverse
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin
from user_model.models import Staff


class StaffDeleteViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_staff_delete(self):
        staff = self.staff_create()
        response = self.supervisor.post(reverse('staff_delete', kwargs={'pk': staff.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/staff/list')
        self.assertFalse(Staff.objects.filter(id=staff.id).exists())
