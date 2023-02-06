from datetime import datetime, timedelta
from management.models import Discount, City, Airport, Airplane, Option, Flight, Ticket
from user_model.models import Staff, User


class DatabaseDataMixin:
    """Creating model instances and returning one instance."""

    def discounts_create(self, number):
        """Creation of a specified number of copies of the model Discount."""
        for num in range(1, number + 1):
            Discount.objects.create(name=f'promo-code{num}',
                                    percents=f'{num}0%',
                                    valid_until=datetime.today().date())

        return Discount.objects.filter(name='promo-code1').first()

    def cities_create(self):
        """Creation of 3 copies of the City model."""
        name_city = (('Kharkov', 'UA'), ('Kiev', 'UA'), ('Kherson', 'UA'))

        for name, country in name_city:
            City.objects.create(name=name,
                                country=country)

        return City.objects.filter(name='Kharkov').first()

    def airport_create(self, city):
        """Creation of an airport in the transferred city."""
        return Airport.objects.create(city=city, name=f'airport-{city.name}', address=f'{city} 19')

    def airplane_create(self):
        """Creates the specified number of airplane."""
        self.cities_create()
        cities = City.objects.all()
        for num in range(3):
            Airplane.objects.create(location=cities[num],
                                    model=f'model{num}',
                                    name=f'Airplane-{num}',
                                    comfort_places=5,
                                    economy_places=5)

        return Airplane.objects.filter(name='Airplane-1').first()

    def users_create(self):
        """
        Registration of two user accounts,
        Returns the list of accounts
        """
        users = []
        for num in range(1, 3):
            users.append(User.objects.create(username=f'testuser{num}',
                                             email=f'testemail{num}@gmail.com',
                                             password='test19'))

        return users

    def staff_create(self):
        """Creates 2 staff."""
        users = self.users_create()
        for num in range(2):
            Staff.objects.create(account=users[num],
                                 position=['gate', 'check-in'][num])

        return Staff.objects.filter(account=users[0]).first()

    def options_create(self):
        """Creating additional and included options."""
        options = (('luggage', 10, 10, 'included'),
                   ('lunch', 10, None, 'included'),
                   ('luggage', 30, 25, 'extra'))

        for option, price, weight, service_type in options:
            Option.objects.create(option=option, price=price, weight=weight, service_type=service_type)

    def data_for_flight_create(self):
        """Creating the data needed to create the flight"""
        self.airplane_create()
        for city in City.objects.all():
            self.airport_create(city)
        self.options_create()

    def __get_city_data(self, city):
        """Get an airport and an airplane in this city."""
        return (Airport.objects.filter(city=city).first(),
                Airplane.objects.filter(location=city).first())

    def flights_create(self):
        """Create two flights."""
        self.data_for_flight_create()
        to_city = City.objects.filter(name='Kharkov').first()
        to_airport = Airport.objects.filter(city=to_city).first()
        departure_date = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
        date_arrival = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M")
        option = Option.objects.filter(option='luggage', service_type='included').first()

        cities = City.objects.all().exclude(name='Kharkov')
        for from_city in cities:
            from_airport, airplane = self.__get_city_data(from_city)
            flight = Flight.objects.create(from_city=from_city,
                                           to_city=to_city,
                                           airplane=airplane,
                                           from_airport=from_airport,
                                           to_airport=to_airport,
                                           departure_date=departure_date,
                                           date_arrival=date_arrival,
                                           flight_time='3h 0min',
                                           price=50)
            flight.option.add(option)

        return Flight.objects.filter(departure_date=departure_date, date_arrival=date_arrival).first()

    def ticket_register(self):
        """Ticket registration."""
        flight = self.flights_create()
        ticket = Ticket.objects.create(flight=flight,
                                       reservation=True,
                                       date_reservation=datetime.now().strftime("%Y-%m-%dT%H:%M"),
                                       first_name='testname19',
                                       last_name='testsurname19',
                                       years_old='adult',
                                       place=1,
                                       price=flight.price,
                                       price_with_options=flight.price,
                                       self_check_in=True,
                                       place_type='economy')

        ticket.included_options.add(flight.option.first())
        return ticket

    def tickets_create(self):
        """Ticket registration by the number of places in economy and comfort classes."""
        flight = self.flights_create()
        option = Option.objects.filter(option='luggage', service_type='extra').first()
        flight.option.add(option)

        for _ in range(flight.airplane.economy_places):
            ticket = Ticket.objects.create(flight=flight, place_type='economy', price=flight.price)
            ticket.included_options.add(flight.option.filter(service_type='included').first())
            ticket.extra_options.add(flight.option.filter(service_type='extra').first())

        return flight

    def ticket_holder(self, owner):
        """Add a ticket holder account and remove self-registration and a place on the ticket."""
        ticket = self.ticket_register()
        ticket.self_check_in = False
        ticket.place = None
        ticket.owner = owner
        ticket.save()
        return ticket
