from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, ListView, DetailView, View
from customer.forms import TicketReservationForm, CustomerForm, TicketRegisterForm, SearchByCodeForm
from customer.utils import send_tickets_by_mail
from management.models import Flight, Ticket, Option, Discount
from management.utils import get_free_place
from user_model.models import User
from datetime import datetime


class Index(View):
    def get(self, request):
        """Home Page."""
        return render(request, 'index.html', {'min_date': str(datetime.today().date())})


class FlightView(View):

    def get(self, request):
        """Search for flights and available tickets."""
        try:
            args = request.GET
            flights = Flight.objects.filter(departure_date__icontains=args['date'],
                                            to_city__name__startswith=args['to_city'],
                                            from_city__name__startswith=args['from_city']
                                            ).select_related(
                'from_city').select_related('to_city').select_related('from_airport').select_related('to_airport')

            filtered_flights = self.get_filtered_flights(flights, args)
            return render(request, 'flights/flight.html', {'min_date': str(datetime.today().date()),
                                                           'initial': args,
                                                           'flights': filtered_flights})
        except Exception:
            return render(request, 'flights/flight.html', {'error': 'Not all fields are filled in for the search.'})

    def get_filtered_flights(self, flights, args):
        """Filter for flights by number of available tickets and price calculation."""
        adults, children, infants = int(args['adults']), int(args['children']), int(args['infants'])

        filtered_flights = []
        for flight in flights:
            tickets = Ticket.objects.filter(flight=flight, reservation=False, place_type=args['class'])
            if len(tickets) >= sum([adults, children, infants]):
                ticket = tickets.first()
                price = sum([ticket.price * adults,
                             ticket.get_price_ticket_child * children,
                             ticket.get_price_ticket_infant * infants])
                included_options = [option['option'] for option in flight.option.filter(service_type='included'
                                                                                        ).values('option')]
                filtered_flights.append([flight, price, len(tickets), included_options])
        return filtered_flights


class FlightReservationView(View):
    def get(self, request, pk):
        """Sending ticket forms to fill out."""
        flight = Flight.objects.filter(pk=pk).select_related('from_city').select_related(
            'to_city').select_related('from_airport').select_related('to_airport').first()
        options = flight.option.all()
        adults, children, infants = self.get_formsets(request.GET)
        ticket = flight.tickets.filter(place_type=request.GET['class']).first()
        price = sum([ticket.price * len(adults),
                     ticket.get_price_ticket_child * len(children),
                     ticket.get_price_ticket_infant * len(infants)])

        return render(request, 'flights/flight_reservation.html', {
            'flight': flight,
            'adults': adults,
            'children': children,
            'infants': infants,
            'price': price,
            'class': request.GET['class'],
            'extra_options': options.filter(service_type='extra'),
            'options': [option['option'] for option in options.filter(service_type='included').values('option')]})

    def post(self, request, pk):
        """If the forms are filled out correctly, they are booked and the tickets are mailed."""
        formset = formset_factory(TicketReservationForm)
        adult, children, infants = (formset(request.POST, prefix='adult'),
                                    formset(request.POST, prefix='children'),
                                    formset(request.POST, prefix='infants'))
        if adult.is_valid() and children.is_valid() and infants.is_valid():
            tickets_id = []
            for forms in [adult, children, infants]:
                tickets_id += self.book_tickets(pk, request.POST['class'], request.user, forms)
            send_tickets_by_mail(tickets_id, request.user)
            return JsonResponse(data={'url': reverse('customer_tickets', kwargs={'pk': request.user.pk})}, status=200)

        errors = self.get_errors(adult, children, infants)
        return JsonResponse(data={'error': errors}, status=401)

    def book_tickets(self, flight_id, place_type, owner, forms):
        """Fills in all ticket data and stores it in the database."""
        tickets = Ticket.objects.filter(flight_id=flight_id, reservation=False, place_type=place_type)[:len(forms)]
        tickets_id = []
        for ticket, form in zip(tickets, forms):
            ticket.owner = owner
            ticket.reservation = True
            ticket.first_name = form.cleaned_data['first_name']
            ticket.last_name = form.cleaned_data['last_name']
            ticket.years_old = forms.prefix
            ticket.date_birthday = form.cleaned_data['date_birthday']
            ticket.gender = form.cleaned_data['gender']
            ticket.document_no = form.cleaned_data['document_no']
            ticket.place_type = place_type
            ticket.date_reservation = datetime.today()
            price = self.get_price_ticket(ticket, forms.prefix)
            ticket.price = price

            if f'{form.prefix}-extra_options' in forms.data:
                extra_options_id = forms.data.getlist(f'{form.prefix}-extra_options')
                price = self.add_extra_options(ticket, price, extra_options_id)
            ticket.price_with_options = price
            ticket.save()
            tickets_id.append(ticket.id)

        return tickets_id

    def get_price_ticket(self, ticket, type_ticket):
        """Returns the price of the ticket by age."""
        if type_ticket == 'adult':
            return ticket.price
        elif type_ticket == 'children':
            return ticket.get_price_ticket_child
        else:
            return ticket.get_price_ticket_infant

    def add_extra_options(self, ticket, price, extra_options_id):
        """Adds all additional options selected to the ticket."""
        options = Option.objects.filter(id__in=extra_options_id)
        for option in options:
            price += option.price
            ticket.extra_options.add(option)
        return price

    def get_errors(self, *formsets):
        """Returns all errors in the ticket forms."""
        return ''.join(set([f'{error.as_text()}\n'
                            for form in formsets if len(form.errors) > 0
                            for errors in form.errors
                            for error in errors.values()]))

    def get_formsets(self, args):
        """Returns sets of forms with age prefixes for the tickets."""
        adult_formset = formset_factory(TicketReservationForm, extra=int(args['adults']))
        children_formset = formset_factory(TicketReservationForm, extra=int(args['children']))
        infants_formset = formset_factory(TicketReservationForm, extra=int(args['infants']))
        return adult_formset(prefix='adult'), children_formset(prefix='children'), infants_formset(prefix='infants')


class CustomerUpdate(UpdateView):
    """Changing account information."""
    model = User
    form_class = CustomerForm
    template_name = 'personal_cabinet/personal_cabinet.html'
    context_object_name = 'customer_update'

    def get_success_url(self):
        return reverse('customer_update', kwargs={'pk': self.kwargs['pk']})


class TicketListView(ListView):
    """List of tickets purchased."""
    model = Ticket
    template_name = 'personal_cabinet/personal_cabinet.html'
    paginate_by = 10

    def get_queryset(self):
        return Ticket.objects.filter(owner=self.kwargs['pk']).select_related(
            'flight__from_city').select_related('flight__to_city').order_by('-date_reservation')


class TicketDetailView(DetailView):
    """Ticket information."""
    model = Ticket
    template_name = 'personal_cabinet/personal_cabinet.html'

    def get_queryset(self):
        return Ticket.objects.filter(pk=self.kwargs['pk']).select_related('flight__from_city').select_related(
            'flight__to_city').select_related('flight__from_airport').select_related('flight__to_airport')


class TicketSearchView(View):
    def get(self, request, **kwargs):
        """Search for a ticket by code."""
        if 'code' in request.GET:
            ticket = Ticket.objects.filter(id=request.GET['code'],
                                           owner=request.user,
                                           self_check_in=False,
                                           check_in=False).first()
            if ticket:
                return redirect('ticket_reg', request.user.id, ticket.id)
            return render(request, 'personal_cabinet/personal_cabinet.html',
                          {'form_search': SearchByCodeForm,
                           'error': 'Unregistered ticket with this code is not found.'})
        return render(request, 'personal_cabinet/personal_cabinet.html', {'form_search': SearchByCodeForm})


class TicketRegisterView(UpdateView):
    """Ticket registration in the personal cabinet.
    (Add a place add a discount)"""
    model = Ticket
    template_name = 'personal_cabinet/personal_cabinet.html'
    form_class = TicketRegisterForm
    context_object_name = 'ticket_reg'

    def form_valid(self, form):
        ticket = self.object
        ticket.place = get_free_place(ticket)
        ticket.self_check_in = True
        if form.data['promo_code'] != '':
            promo_code = Discount.objects.filter(name=form.data['promo_code']).first()
            ticket.price_with_options = ticket.price_with_options * (
                    100 - int(promo_code.percents.replace('%', ''))) / 100
            ticket.discount = promo_code
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ticket_detail', kwargs={'id': self.kwargs['id'], 'pk': self.kwargs['pk']})
