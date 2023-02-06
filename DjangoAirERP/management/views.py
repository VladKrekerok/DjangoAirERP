from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DeleteView, ListView, CreateView, DetailView, FormView, UpdateView
from customer.forms import SearchByCodeForm
from user_model.models import Staff, User
from .permissions import (SupervisorPermission, CheckInManagerPermission,
                          GateManagerPermission, AllStaffPermission)
from .models import Flight, Ticket, Option, City, Airport, Airplane, Discount
from .utils import get_free_place
from .forms import (FlightForm, SearchFlightsForm, StaffForm, CitiesFilterForm, AirportForm, CityForm,
                    AirplaneForm, FlightRegistryForm, StaffUpdateForm, DiscountFrom, CheckInForm)


class GateManagerView(GateManagerPermission, View):
    raise_exception = True

    def post(self, request, pk):
        """Check-in for boarding, begins one hour before departure."""
        ticket = Ticket.objects.filter(id=pk).first()
        departure_date = ticket.flight.departure_date
        if departure_date > datetime.today() and departure_date - timedelta(hours=1) <= datetime.today():
            if ticket.check_in:
                ticket.boarding = True
                ticket.boarding_time = datetime.today()
                ticket.save()
                return render(request, 'ticket_by_code/search_ticket.html',
                              {'form': SearchByCodeForm, 'ticket': ticket})
            error_landing = 'Your ticket did not check in.'
            return render(request, 'ticket_by_code/search_ticket.html', {'form': SearchByCodeForm,
                                                                         'ticket': ticket,
                                                                         'error_landing': error_landing})
        error_landing = 'Check-in for boarding begins one hour before departure.'
        return render(request, 'ticket_by_code/search_ticket.html', {'form': SearchByCodeForm,
                                                                     'ticket': ticket,
                                                                     'error_landing': error_landing})


class CheckInManagerView(CheckInManagerPermission, UpdateView):
    """Ticket check-in, adding luggage weight and the ability to add more options."""
    raise_exception = True

    model = Ticket
    template_name = 'check_in_manager/check_in.html'
    form_class = CheckInForm
    success_url = reverse_lazy('search_ticket')

    def get_queryset(self):
        """Adds additional options that are included for the flight and have not yet been added to the ticket."""
        ticket = Ticket.objects.filter(id=self.kwargs['pk'])
        extra_options = Option.objects.filter(flight=ticket[0].flight, service_type='extra'
                                              ).exclude(option__in=ticket[0].extra_options.all().values('option'))
        self.extra_context = {'extra_options': extra_options}
        return ticket

    def form_valid(self, form):
        if 'extra_options' in self.request.POST:
            options = Option.objects.filter(id__in=form.data.getlist('extra_options'))
            price = self.object.price_with_options
            self.object.price_with_options = self.add_options_and_price(options, price)

        if not self.object.place:
            self.object.place = get_free_place(self.object)
        self.object.payment_status = True
        self.object.check_in = True
        self.object = form.save()
        return super().form_valid(form)

    def add_options_and_price(self, options, price):
        """Adding options and price to a ticket."""
        for option in options:
            price += option.price
            self.object.extra_options.add(option)
        return price


class TicketSearchView(AllStaffPermission, View):
    raise_exception = True

    def get(self, request):
        """Search for an active booked tickets."""
        if 'code' in request.GET:
            ticket = Ticket.objects.filter(id=request.GET['code'],
                                           flight__date_arrival__gte=datetime.today(),
                                           reservation=True).first()
            if ticket:
                return render(request, 'ticket_by_code/search_ticket.html', {'form': SearchByCodeForm,
                                                                             'ticket': ticket})
            error = 'The ticket code is not valid or the flight is already closed.'
            return render(request, 'ticket_by_code/search_ticket.html', {'form': SearchByCodeForm, 'error': error})
        return render(request, 'ticket_by_code/search_ticket.html', {'form': SearchByCodeForm})


class FlightsFilterView(SupervisorPermission, View):
    raise_exception = True

    def get(self, request):
        """Filtering flights by cities and departure date."""
        args = request.GET
        if 'from_city' in args and 'to_city' in args:
            from_city = City.objects.filter(name=args['from_city']).first()
            to_city = City.objects.filter(name=args['to_city']).first()
            if 'departure_date' in args and args['departure_date'] != '':
                object_list = Flight.objects.filter(from_city=from_city,
                                                    to_city=to_city,
                                                    date_arrival__gt=datetime.today(),
                                                    departure_date__icontains=args['departure_date']).select_related(
                    'from_city').select_related('to_city').select_related('airplane').select_related(
                    'from_airport').select_related('to_airport')
            else:
                object_list = Flight.objects.filter(from_city=from_city,
                                                    to_city=to_city,
                                                    date_arrival__gt=datetime.today()).select_related(
                    'from_city').select_related('to_city').select_related(
                    'airplane').select_related('from_airport').select_related('to_airport')
        else:
            object_list = None
        return render(request, 'flight/flights_list.html', {'object_list': object_list, 'form': SearchFlightsForm})


class FlightTicketsView(AllStaffPermission, View):
    raise_exception = True

    def get(self, request):
        """By Flight Code returns a list of tickets."""
        if 'code' in request.GET:
            flight = Flight.objects.filter(id=request.GET['code'], date_arrival__gte=datetime.today()).select_related(
                'from_city').select_related('to_city').first()
            if flight:
                return render(request, 'flight/flight_tickets.html', {'form': SearchByCodeForm,
                                                                      'flight': flight})
            error = 'The flight code is not valid or the flight is already closed.'
            return render(request, 'flight/flight_tickets.html', {'form': SearchByCodeForm, 'error': error})
        return render(request, 'flight/flight_tickets.html', {'form': SearchByCodeForm})


class FlightsListView(SupervisorPermission, ListView):
    raise_exception = True
    model = Flight
    queryset = Flight.objects.filter(date_arrival__gt=datetime.today()).select_related(
        'from_city').select_related('to_city').select_related('airplane').select_related('from_airport'
                                                                                         ).select_related('to_airport')
    template_name = 'flight/flights_list.html'
    extra_context = {'form': SearchFlightsForm}
    paginate_by = 10


class FlightCreateView(SupervisorPermission, FormView):
    raise_exception = True
    form_class = FlightForm
    template_name = 'flight/flight_form.html'

    def get(self, request, *args, **kwargs):
        """Returns a form with data on the requested cities, their airports and available airplanes."""
        args = request.GET
        if args:
            form = FlightForm(args)
            if form.is_valid():
                from_city = City.objects.filter(id=args['from_city']).first()
                to_city = City.objects.filter(id=args['to_city']).first()
                airplanes = Airplane.objects.filter(Q(location=from_city), ~Q(busy_date__gt=args['departure_date']))
                from_airport = Airport.objects.filter(city_id=from_city)
                to_airport = Airport.objects.filter(city_id=to_city)
                return render(request, 'flight/flight_add.html', {'form': FlightRegistryForm,
                                                                  'from_city': from_city,
                                                                  'to_city': to_city,
                                                                  'airplanes': airplanes,
                                                                  'from_airport': from_airport,
                                                                  'to_airport': to_airport,
                                                                  'initial': args})
            return self.form_invalid(form)
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """Registration of the flight and tickets to it."""
        args = request.POST
        try:
            flight_time = self.get_flight_time(args['departure_date'], args['date_arrival'])
            from_city = City.objects.filter(name=' '.join(args['from_city'].split(' ')[:-1]),
                                            country=args['from_city'].split(' ')[-1]).first()
            to_city = City.objects.filter(name=' '.join(args['to_city'].split(' ')[:-1]),
                                          country=args['to_city'].split(' ')[-1]).first()
            flight = Flight.objects.create(airplane_id=args['airplane_id'],
                                           from_city=from_city,
                                           to_city=to_city,
                                           from_airport_id=args['from_airport_id'],
                                           to_airport_id=args['to_airport_id'],
                                           price=args['price'],
                                           flight_time=flight_time,
                                           departure_date=args['departure_date'],
                                           date_arrival=args['date_arrival'])

            options = request.POST.getlist('option')
            if options:
                self.add_options(options, flight)
            Airplane.objects.filter(id=args['airplane_id']).update(busy_date=args['date_arrival'], location=to_city)
            self.ticket_registration(flight)

            return JsonResponse(data={'pk': request.user.pk}, status=200)
        except Exception:
            return JsonResponse(data={'error': 'Not all fields are filled in.'}, status=400)

    def ticket_registration(self, flight):
        """Ticket registration by the number of places in economy and comfort classes."""
        comfort_places = flight.airplane.comfort_places
        economy_places = flight.airplane.economy_places
        tickets = []
        for _ in range(comfort_places):
            tickets.append(Ticket.objects.create(flight=flight, place_type='comfort', price=float(flight.price) * 1.5))
        for _ in range(economy_places):
            tickets.append(Ticket.objects.create(flight=flight, place_type='economy', price=flight.price))

        option_included = flight.option.filter(service_type='included')
        self.add_included_options(tickets, option_included)

    def add_included_options(self, tickets, option_included):
        """Adds all included options to the flight tickets."""
        for option in option_included:
            for ticket in tickets:
                ticket.included_options.add(option)

    def add_options(self, options_id, flight):
        """Adds options to the flight."""
        options = Option.objects.filter(id__in=options_id)
        for option in options:
            flight.option.add(option)

    def get_flight_time(self, departure_date, date_arrival):
        """Returns the flight time."""
        delta = datetime.strptime(date_arrival, "%Y-%m-%dT%H:%M") - datetime.strptime(departure_date, "%Y-%m-%dT%H:%M")
        hour = (delta.seconds // 3600) + delta.days * 24
        minutes = delta.seconds % 3600 // 60
        return f'{hour}h {minutes}min'


class FlightDeleteView(SupervisorPermission, DeleteView):
    raise_exception = True

    model = Flight
    success_url = reverse_lazy('flights_list')


class FlightDetailView(SupervisorPermission, DetailView):
    raise_exception = True

    model = Flight
    template_name = 'flight/flight_detail.html'

    def get_queryset(self):
        return Flight.objects.filter(pk=self.kwargs['pk']).select_related(
            'from_city').select_related('airplane').select_related('to_city').select_related(
            'from_airport').select_related('to_airport')


class StaffListView(SupervisorPermission, ListView):
    raise_exception = True

    model = Staff
    queryset = Staff.objects.all().select_related('account')
    template_name = 'staff/staff_list.html'
    paginate_by = 10


class StaffCreateView(SupervisorPermission, FormView):
    raise_exception = True

    form_class = StaffForm
    template_name = 'staff/staff_add.html'
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        user = User.objects.create(email=form.data['email'], password=make_password(password=form.data['password1']))
        Staff.objects.create(account_id=user.id, position=form.data['position'])
        return super().form_valid(form)


class StaffUpdateView(SupervisorPermission, UpdateView):
    raise_exception = True

    model = Staff
    template_name = 'staff/staff_update.html'
    form_class = StaffUpdateForm
    success_url = reverse_lazy('staff_list')


class StaffDeleteView(SupervisorPermission, DeleteView):
    raise_exception = True

    model = Staff
    success_url = reverse_lazy('staff_list')


class CityCreateView(SupervisorPermission, CreateView):
    raise_exception = True

    model = City
    form_class = CityForm
    template_name = 'city/city_add.html'
    success_url = reverse_lazy('cities_list')


class CitiesListView(SupervisorPermission, ListView):
    raise_exception = True

    model = City
    template_name = 'city/cities_list.html'
    extra_context = {'form': CitiesFilterForm}
    paginate_by = 20


class CitiesFilterView(SupervisorPermission, View):
    raise_exception = True

    def get(self, request):
        """Filtering cities by name and country."""
        args = request.GET
        if 'name' in args and 'country' in args:
            object_list = City.objects.filter(name__startswith=args['name'].title(),
                                              country__startswith=args['country'].upper())
        else:
            object_list = None
        return render(request, 'city/cities_list.html', {'form': CitiesFilterForm, 'object_list': object_list})


class CityDetailView(SupervisorPermission, DetailView):
    raise_exception = True

    model = City
    template_name = 'city/city_detail.html'

    def get_queryset(self):
        airports = Airport.objects.filter(city_id=self.kwargs['pk'])
        self.extra_context = {'airports': airports}
        return City.objects.filter(pk=self.kwargs['pk'])


class CityDeleteView(SupervisorPermission, DeleteView):
    raise_exception = True

    model = City
    success_url = reverse_lazy('cities_list')


class AirportCreateView(SupervisorPermission, FormView):
    raise_exception = True

    form_class = AirportForm
    template_name = 'city/airport_add.html'

    def form_valid(self, form):
        Airport.objects.create(city_id=self.kwargs['pk'],
                               name=form.cleaned_data['name'],
                               address=form.cleaned_data['address'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('city_detail', kwargs={'pk': self.kwargs['pk']})


class AirplaneCreateView(SupervisorPermission, CreateView):
    raise_exception = True

    model = Airplane
    template_name = 'airplane/airplane_add.html'
    form_class = AirplaneForm
    success_url = reverse_lazy('airplane_list')


class AirplaneListView(SupervisorPermission, ListView):
    raise_exception = True

    model = Airplane
    queryset = Airplane.objects.all().select_related('location')
    template_name = 'airplane/airplane_list.html'
    paginate_by = 10


class AirplaneDeleteView(SupervisorPermission, DeleteView):
    raise_exception = True

    model = Airplane
    success_url = reverse_lazy('airplane_list')


class AirplaneUpdateView(SupervisorPermission, UpdateView):
    raise_exception = True

    model = Airplane
    template_name = 'airplane/airplane_update.html'
    form_class = AirplaneForm
    success_url = reverse_lazy('airplane_list')


class DiscountCreateView(SupervisorPermission, CreateView):
    raise_exception = True

    model = Discount
    form_class = DiscountFrom
    template_name = 'discount/discount_add.html'
    success_url = reverse_lazy('discount_list')


class DiscountListView(SupervisorPermission, ListView):
    raise_exception = True

    model = Discount
    template_name = 'discount/discount_list.html'
    paginate_by = 10


class DiscountUpdateView(SupervisorPermission, UpdateView):
    raise_exception = True

    model = Discount
    template_name = 'discount/discount_update.html'
    form_class = DiscountFrom
    success_url = reverse_lazy('discount_list')


class DiscountDeleteView(SupervisorPermission, DeleteView):
    raise_exception = True

    model = Discount
    success_url = reverse_lazy('discount_list')
