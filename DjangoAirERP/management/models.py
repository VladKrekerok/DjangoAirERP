from django.core.validators import MinValueValidator, MinLengthValidator, RegexValidator
from django.db import models
from management.validators import min_date_validator
from user_model.models import User


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=2)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} {self.country}'


class Airplane(models.Model):
    location = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cities')
    model = models.CharField(max_length=200)
    name = models.CharField(max_length=200, unique=True)
    comfort_places = models.IntegerField(validators=[MinValueValidator(limit_value=1,
                                                                       message='Minimum number of places 1.')])
    economy_places = models.IntegerField(validators=[MinValueValidator(limit_value=1,
                                                                       message='Minimum number of places 1.')])
    date_registration = models.DateField(auto_now_add=True)
    busy_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Airport(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='airports')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Option(models.Model):
    SERVICE_TYPE = {
        ('included', 'Included'),
        ('extra', 'Extra')
    }
    option = models.CharField(max_length=100)
    price = models.FloatField(validators=[MinValueValidator(limit_value=1, message='Minimum number of seats 1.')])
    weight = models.IntegerField(null=True)
    service_type = models.CharField(max_length=8, choices=SERVICE_TYPE, null=True)

    def __str__(self):
        if self.weight:
            return f'{self.option} {self.weight}kg - {self.service_type}'
        return f'{self.option} - {self.service_type}'


class Flight(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_city')
    from_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='from_airport')
    to_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='to_airport')
    departure_date = models.DateTimeField(validators=[min_date_validator])
    date_arrival = models.DateTimeField(validators=[min_date_validator])
    flight_time = models.CharField(max_length=20)
    option = models.ManyToManyField(Option)
    date_registration = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(validators=[MinValueValidator(limit_value=1, message='Minimum number of seats 1.')])

    class Meta:
        ordering = ('-date_registration',)

    def __str__(self):
        return f'{self.from_city} --> {self.to_city}'


class Discount(models.Model):
    name = models.CharField(unique=True, max_length=20)
    percents = models.CharField(max_length=4)
    valid_until = models.DateField()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.percents


class Ticket(models.Model):
    PASSENGER = (
        ('adult', 'Adult'),
        ('child ', 'Child'),
        ('infant', 'Infant')
    )

    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    PLACE_TYPE = (
        ('economy', 'Economy'),
        ('comfort', 'Comfort')
    )

    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='purchases')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    reservation = models.BooleanField(default=False)
    date_reservation = models.DateTimeField(null=True)
    first_name = models.CharField(null=True, max_length=30,
                                  validators=[MinLengthValidator(limit_value=1, message='Minimum length 1 character.')])
    last_name = models.CharField(null=True, max_length=30,
                                 validators=[MinLengthValidator(limit_value=1, message='Minimum length 1 character.')])
    years_old = models.CharField(null=True, max_length=8, choices=PASSENGER)
    place = models.IntegerField(null=True,
                                validators=[MinValueValidator(limit_value=1, message='Minimum number of seats 1.')])
    price = models.FloatField(validators=[MinValueValidator(limit_value=1, message='Minimum number of seats 1.')])
    price_with_options = models.FloatField(null=True, validators=[
        MinValueValidator(limit_value=1, message='Minimum number of seats 1.')])
    date_birthday = models.DateField(null=True)
    gender = models.CharField(max_length=6, choices=GENDER, null=True, default=None)
    document_no = models.CharField(max_length=8, null=True, validators=[RegexValidator(
        regex=r"[A-Za-z]{2}[0-9]{6}",
        message='The form is filled in with the first two letters and six digits.')])
    payment_status = models.BooleanField(default=False)
    check_in = models.BooleanField(default=False)
    self_check_in = models.BooleanField(default=False)
    place_type = models.CharField(max_length=7, choices=PLACE_TYPE)
    discount = models.ForeignKey(Discount, blank=True, null=True, on_delete=models.CASCADE, related_name='discounts')
    included_options = models.ManyToManyField(Option, blank=True, related_name='included_options')
    extra_options = models.ManyToManyField(Option, blank=True, related_name='extra_options')
    luggage_weight = models.IntegerField(null=True)
    boarding = models.BooleanField(default=False)
    boarding_time = models.DateTimeField(null=True)

    @property
    def get_price_ticket_child(self):
        return round(self.price * 0.5, 2)

    @property
    def get_price_ticket_infant(self):
        return round(self.price * 0.1, 2)

    @property
    def get_place(self):
        if self.place:
            return self.place
        return 'Not registered'
