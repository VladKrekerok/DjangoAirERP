from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from user_model.models import Staff, User
from .models import Flight, City, Airport, Airplane, Discount, Ticket, Option


class FlightRegistryForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ('option', 'price')
        widgets = {
            'option': forms.CheckboxSelectMultiple(),
            'price': forms.TextInput(attrs={'type': 'number',
                                            'min': 1,
                                            'placeholder': "Price per place"})
        }
        labels = {'option': '',
                  'price': ''}


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ('from_city', 'to_city', 'departure_date', 'date_arrival')
        widgets = {
            'departure_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_arrival': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean(self):
        departure_date = self.cleaned_data['departure_date']
        date_arrival = self.cleaned_data['date_arrival']
        from_city = self.cleaned_data['from_city']
        to_city = self.cleaned_data['to_city']

        if departure_date > date_arrival:
            raise ValidationError('Departure time cannot be less than arrival time!')
        elif from_city.id == to_city.id:
            raise ValidationError('Cities of departure and arrival cannot be the same.')
        return self.cleaned_data


class SearchFlightsForm(forms.Form):
    STATUS_TICKETS = (
        (False, 'Unregistered tickets'),
        (True, 'Registered tickets'),
    )

    from_city = forms.CharField(max_length=200, label='', widget=forms.TextInput(
        attrs={'class': 'flight-filter', 'placeholder': "From city"}))
    to_city = forms.CharField(max_length=200, label='', widget=forms.TextInput(
        attrs={'class': 'flight-filter', 'placeholder': "To city"}))
    departure_date = forms.DateTimeField(label='', required=False, widget=forms.DateTimeInput(
        attrs={'class': 'flight-filter', 'type': 'date', 'min': datetime.today().date()}))


class StaffForm(forms.ModelForm):
    email = forms.EmailField(label="Email", max_length=254)
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repeat password", strip=False, widget=forms.PasswordInput())

    class Meta:
        model = Staff
        fields = ('email', 'password1', 'password2', 'position')

    def clean(self):
        try:
            validate_email(self.cleaned_data['email'])
            user = User.objects.filter(email=self.cleaned_data['email']).first()
        except Exception:
            raise ValidationError('Email is not valid')
        if user:
            raise ValidationError('An account with this email already exists.')
        elif self.cleaned_data['password1'] and self.cleaned_data['password2'] and \
                self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError('Passwords are not the same.')
        return self.cleaned_data


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('position',)


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

    def clean(self):
        try:
            country = self.cleaned_data['country']
            city_name = self.cleaned_data['name']
        except Exception:
            raise ValidationError('Parameters are not specified.')
        if not country.isalpha() or len(country) != 2:
            raise ValidationError('The name of the country must consist of two letters.')

        city = City.objects.filter(name=city_name, country=country.upper()).first()
        if city:
            raise ValidationError('A city with that name is already registered in this country.')
        return self.cleaned_data


class CitiesFilterForm(forms.Form):
    name = forms.CharField(max_length=200, label='', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "City name"}))
    country = forms.CharField(max_length=200, label='', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Country of the city"}))


class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ('name', 'address')

    def clean(self):
        name = self.cleaned_data['name']
        address = self.cleaned_data['address']
        if Airport.objects.filter(name=name, address=address).exists():
            raise ValidationError('An airport with this name and address is already registered.')
        return self.cleaned_data


class AirplaneForm(forms.ModelForm):
    class Meta:
        model = Airplane
        fields = '__all__'


class DiscountFrom(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'
        widgets = {
            'valid_until': forms.DateTimeInput(attrs={'type': 'date', 'min': datetime.today().date()})
        }

    def clean_percents(self):
        percents = self.cleaned_data['percents']
        if percents.count('%') != 1:
            raise ValidationError('The discount is indicated in %')
        elif int(percents.replace('%', '')) == 0:
            raise ValidationError('Incorrect value')
        elif len(percents) == 4 and int(percents[:3]) > 100 and len(percents) < 5:
            raise ValidationError('Maximum value is 100%')
        return self.cleaned_data['percents']


class CheckInForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('luggage_weight',)
        widgets = {
            'luggage_weight': forms.TextInput(attrs={'min': 0, 'type': 'number'})
        }

    def clean_luggage_weight(self):
        luggage_weight = self.cleaned_data['luggage_weight']

        included_weight = self.instance.included_options.filter(option__icontains='Luggage').values('weight')
        extra_options_weight = self.instance.extra_options.filter(option__icontains='Luggage').values('weight')
        add_options = Option.objects.filter(id__in=self.data.getlist('extra_options')).values('weight')

        max_width = sum([option['weight'] for option in included_weight] +
                        [option['weight'] for option in extra_options_weight] +
                        [option['weight'] for option in add_options])
        if max_width < luggage_weight:
            raise ValidationError('Baggage weight exceeds the weight limit on the ticket.')
        return luggage_weight
