from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    GENDER = (
        ('male', 'male'),
        ('female', 'female')
    )

    username = models.CharField(null=True, max_length=150)
    birthday = models.DateField(blank=True, null=True, verbose_name='Birthday')
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER, verbose_name='Gender')
    email = models.EmailField(_("Email"), unique=True)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def get_name(self):
        if self.first_name:
            return self.first_name
        return '-----'

    @property
    def get_surname(self):
        if self.first_name:
            return self.last_name
        return '-----'


class Staff(models.Model):
    ROLES = (
        ('gate', 'Gate manager'),
        ('check-in', 'Check-in manager'),
        ('supervisor', 'Supervisor')
    )

    position = models.CharField(max_length=10, choices=ROLES, null=True, default=None)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    date_accession = models.DateField(auto_now_add=True)
