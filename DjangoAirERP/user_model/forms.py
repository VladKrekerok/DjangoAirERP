from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class AuthenticationForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'form-control'}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control'}),
    )


class UserForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label=_("Repeat password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")
