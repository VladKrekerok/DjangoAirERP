from django.urls import path
from .views import (Index, FlightView, FlightReservationView, CustomerUpdate, TicketListView,
                    TicketDetailView, TicketRegisterView, TicketSearchView)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('flights/search', FlightView.as_view(), name='flights_search'),
    path('flights/<int:pk>/reservation', FlightReservationView.as_view(), name='flights_reservation'),
    path('cabinet/<int:pk>/update', CustomerUpdate.as_view(), name='customer_update'),
    path('cabinet/<int:pk>/tickets', TicketListView.as_view(), name='customer_tickets'),
    path('cabinet/<int:id>/tickets/<int:pk>', TicketDetailView.as_view(), name='ticket_detail'),
    path('cabinet/<int:id>/tickets/search', TicketSearchView.as_view(), name='ticket_search'),
    path('cabinet/<int:id>/tickets/<int:pk>/register', TicketRegisterView.as_view(), name='ticket_reg'),
]
