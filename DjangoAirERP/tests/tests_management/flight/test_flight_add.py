from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from management.models import Airport, City, Airplane, Option, Flight
from mixin_data import DatabaseDataMixin
from mixin_login import SupervisorMixin


class FlightCreateViewTest(SupervisorMixin, DatabaseDataMixin, TestCase):
    def test_get_flight_add(self):
        self.data_for_flight_create()
        from_city, to_city = City.objects.filter(name__in=['Kharkov', 'Kherson'])

        response = self.supervisor.get(reverse('flight_add'),
                                       data={'from_city': from_city.id,
                                             'to_city': to_city.id,
                                             'departure_date': datetime.today() + timedelta(hours=2),
                                             'date_arrival': datetime.today() + timedelta(hours=5)})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Kharkov UA', str(response.content))
        self.assertIn('Kherson UA', str(response.content))
        self.assertIn(str((datetime.today() + timedelta(hours=2)).date()), str(response.content))
        self.assertIn('Airplane-0', str(response.content))
        self.assertIn('airport-Kharkov', str(response.content))
        self.assertIn('airport-Kherson', str(response.content))
        self.assertIn('lunch - included', str(response.content))
        self.assertIn('luggage 10kg - included', str(response.content))

    def test_post_flight_add(self):
        self.data_for_flight_create()
        from_city, to_city = City.objects.filter(name__in=['Kharkov', 'Kherson'])
        from_airport = Airport.objects.filter(city=from_city).first()
        to_airport = Airport.objects.filter(city=to_city).first()
        airplane = Airplane.objects.filter(location=from_city).first()
        option = Option.objects.all().first()
        departure_date = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
        date_arrival = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M")

        response = self.supervisor.post(reverse('flight_add'), data={
            'from_city': from_city,
            'to_city': to_city,
            'departure_date': departure_date,
            'date_arrival': date_arrival,
            'airplane_id': airplane.id,
            'from_airport_id': from_airport.id,
            'to_airport_id': to_airport.id,
            'option': option.id,
            'price': 50
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Flight.objects.filter(from_city=from_city,
                                              to_city=to_city,
                                              departure_date__gte=departure_date,
                                              date_arrival__gte=date_arrival,
                                              airplane=airplane,
                                              from_airport=from_airport,
                                              to_airport=to_airport,
                                              option=option,
                                              price=50).exists())
