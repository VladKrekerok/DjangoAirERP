from django.test import TestCase
from django.urls import reverse

from user_model.models import User


class LoginTest(TestCase):
    def test_login(self):
        self.user = User.objects.create_user(email='test19@gmail.com', username='username_test', password='test19qwe')
        response = self.client.post(reverse('login'),
                                    data={'email': 'test19@gmail.com', 'password': 'test19qwe'})

        self.assertEqual(response.status_code, 200)
