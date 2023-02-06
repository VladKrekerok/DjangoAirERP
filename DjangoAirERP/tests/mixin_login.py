from django.test import Client, TestCase

from user_model.models import User, Staff


class UserMixin:
    """Create a user."""

    def setUp(self):
        self.user = User.objects.create_user(username='test19', email='test19@gmail.com', password='test19')


class AuthClientMixin(UserMixin, TestCase):
    """Authorized user."""

    def setUp(self):
        super().setUp()
        self.auth_client = Client()
        self.auth_client.login(username='test19', gmail='test19@gmail.com', password='test19')


class SupervisorMixin(UserMixin, TestCase):
    """Employee with the position of supervisor."""

    def setUp(self):
        super().setUp()
        self.staff = Staff.objects.create(position='supervisor', account=self.user)
        self.supervisor = Client()
        self.supervisor.login(username='test19', gmail='test19@gmail.com', password='test19')


class CheckInManagerMixin(UserMixin, TestCase):
    """Employee with the position of check-in manager."""

    def setUp(self):
        super().setUp()
        self.staff = Staff.objects.create(position='check-in', account=self.user)
        self.check_in = Client()
        self.check_in.login(username='test19', gmail='test19@gmail.com', password='test19')


class GateManagerMixin(UserMixin, TestCase):
    """Employee with the position of gate manager."""

    def setUp(self):
        super().setUp()
        self.staff = Staff.objects.create(position='gate', account=self.user)
        self.gate = Client()
        self.gate.login(username='test19', gmail='test19@gmail.com', password='test19')
