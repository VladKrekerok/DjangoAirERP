from django.test import TestCase
from django.urls import reverse
from mixin_login import SupervisorMixin
from user_model.models import User


class StaffCreateViewTest(SupervisorMixin, TestCase):
    def test_staff_add(self):
        response = self.supervisor.post(reverse('staff_add'), data={'email': 'staff@gmail.com',
                                                                    'password1': 'test123',
                                                                    'password2': 'test123',
                                                                    'position': 'check-in'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/management/staff/list')
        self.assertTrue(User.objects.filter(email='staff@gmail.com', staff__position='check-in').exists())
