from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from management.models import Ticket, Discount
from user_model.models import User


class TicketReservationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('first_name', 'last_name', 'gender', 'document_no', 'date_birthday')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-ticket', 'required': 'required',
                                                 'placeholder': "First name"}),
            'last_name': forms.TextInput(attrs={'class': 'input-ticket', 'required': 'required',
                                                'placeholder': "Last name"}),
            'gender': forms.Select(attrs={'class': 'input-ticket', 'required': 'required',
                                          'placeholder': "Gender"}),
            'document_no': forms.TextInput(attrs={'class': 'input-ticket', 'required': 'required',
                                                  'pattern': '[A-Za-z]{2}[0-9]{6}',
                                                  'oninvalid': "this.setCustomValidity('This field is required, "
                                                               "the format is 2 letters and 6 digits.')",
                                                  'oninput': "setCustomValidity('')", 'placeholder': "Document no"}),
            'date_birthday': forms.DateInput(attrs={'class': 'input-ticket', 'max': datetime.today().date(),
                                                    'min': datetime.today().date() - timedelta(days=365 * 95),
                                                    'onfocus': "this.type='date'", 'placeholder': "Date birthday",
                                                    'required': 'required'})
        }
        labels = {'first_name': '',
                  'last_name': '',
                  'gender': '',
                  'document_no': '',
                  'date_birthday': ''
                  }

    def clean_document_no(self):
        document_no = self.cleaned_data['document_no']
        if not document_no[0:2].isalpha() or not document_no[2:].isdigit():
            raise ValidationError(
                "Incorrectly filled out passport number, the form of filling the 2 first letters and 6 digits.")
        return document_no

    def clean_date_birthday(self):
        date_birthday = self.cleaned_data['date_birthday']
        years_old = self.prefix
        date_today = datetime.today().date()
        date_for_12_age = datetime.strptime(
            f'{date_today.year - 12}:{date_today.month}:{date_today.day}', "%Y:%m:%d").date()
        date_for_2_age = datetime.strptime(
            f'{date_today.year - 2}:{date_today.month}:{date_today.day}', "%Y:%m:%d").date()

        if 'adult' in years_old:
            if date_birthday >= date_for_12_age:
                raise ValidationError("Error, the age for an adult ticket must be over 12 years old.")
        elif 'children' in years_old:
            if date_for_12_age < date_birthday > date_for_2_age:
                raise ValidationError("Error, the age for a children ticket from 2 years to 12.")
        else:
            if date_birthday <= date_for_2_age:
                raise ValidationError("Error, the age for a children ticket must be under 2 years old.")
        return date_birthday


class TicketRegisterForm(forms.ModelForm):
    promo_code = forms.CharField(max_length=20, label='', required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'promo-code', 'placeholder': "Promo code for a discount"}))

    class Meta:
        model = Ticket
        fields = ('promo_code',)

    def clean_promo_code(self):
        promo_code = self.cleaned_data['promo_code']
        if promo_code != '':
            if not Discount.objects.filter(name=promo_code).exists():
                raise ValidationError("Unfortunately, such a promo code is not found, you can continue without.")
        return promo_code


class SearchByCodeForm(forms.Form):
    code = forms.IntegerField(min_value=1, label='', widget=forms.TextInput(attrs={'class': 'customer-input',
                                                                                   'type': 'number',
                                                                                   'placeholder': 'Code'}))


class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthday', 'gender')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'customer-input',
                                                 'placeholder': "First name"}),
            'last_name': forms.TextInput(attrs={'class': 'customer-input',
                                                'placeholder': "Last name"}),
            'birthday': forms.DateInput(attrs={'class': 'customer-input', 'max': datetime.today().date(),
                                               'min': datetime.today().date() - timedelta(days=365 * 95),
                                               'onfocus': "this.type='date'", 'placeholder': "Date birthday"}),
            'email': forms.TextInput(attrs={'class': 'customer-input',
                                            'placeholder': "Email"}),
            'gender': forms.Select(attrs={'class': 'customer-input',
                                          'placeholder': "Gender"}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'birthday': '',
            'email': '',
            'gender': ''
        }
