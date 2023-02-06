from django.test import TestCase
from django.urls import reverse
from mixin_login import AuthClientMixin


class IndexTest(AuthClientMixin, TestCase):
    def test_index(self):
        response = self.auth_client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Where from', str(response.content))
        self.assertIn('Where to', str(response.content))
        self.assertIn('date', str(response.content))
        self.assertIn('Passengers', str(response.content))
        self.assertIn('Economy', str(response.content))
