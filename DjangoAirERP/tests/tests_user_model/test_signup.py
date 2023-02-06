from django.test import TestCase
from django.urls import reverse

from user_model.models import User


class SignUpTest(TestCase):
    def test_SignUp(self):
        response = self.client.post(reverse('signup'), data={'email': 'test19@gmail.com',
                                                             'password1': 'test19password',
                                                             'password2': 'test19password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='test19@gmail.com').exists())
