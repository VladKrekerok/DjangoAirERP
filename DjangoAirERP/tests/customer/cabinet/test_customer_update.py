from django.test import TestCase
from django.urls import reverse
from mixin_login import AuthClientMixin
from user_model.models import User


class CustomerUpdateTest(AuthClientMixin, TestCase):
    def test_customer_update(self):
        response = self.auth_client.post(reverse('customer_update', kwargs={'pk': self.user.pk}),
                                         data={'first_name': 'new-name',
                                               'last_name': 'new-surname',
                                               'email': 'newemail@gmail.com',
                                               'gender': 'male'})

        updated = User.objects.filter(id=self.user.id).first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/cabinet/{self.user.id}/update')
        self.assertEqual(updated.first_name, 'new-name')
        self.assertEqual(updated.last_name, 'new-surname')
        self.assertEqual(updated.email, 'newemail@gmail.com')
        self.assertEqual(updated.gender, 'male')
