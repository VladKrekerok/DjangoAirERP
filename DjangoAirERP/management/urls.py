from django.urls import path
from .views import (FlightCreateView, FlightsListView, FlightsFilterView,
                    FlightDeleteView, FlightDetailView, StaffCreateView,
                    StaffListView, StaffUpdateView, StaffDeleteView,
                    CityCreateView, CitiesListView, CitiesFilterView,
                    CityDetailView, AirportCreateView, CityDeleteView,
                    AirplaneCreateView, AirplaneListView, AirplaneUpdateView,
                    AirplaneDeleteView, DiscountCreateView, DiscountListView,
                    DiscountUpdateView, DiscountDeleteView, GateManagerView,
                    TicketSearchView, CheckInManagerView, FlightTicketsView)

urlpatterns = [
    path('tickets/search', TicketSearchView.as_view(), name='search_ticket'),
    path('tickets/<int:pk>/check-in', CheckInManagerView.as_view(), name='check_in'),
    path('tickets/<int:pk>/landing', GateManagerView.as_view(), name='tickets_landing'),

    path('flights', FlightCreateView.as_view(), name='flight_add'),
    path('flights/list', FlightsListView.as_view(), name='flights_list'),
    path('flights/tickets', FlightTicketsView.as_view(), name='flight_tickets'),
    path('flights/list/filter', FlightsFilterView.as_view(), name='flights_filter'),
    path('flights/<int:pk>/delete', FlightDeleteView.as_view(), name='flight_delete'),
    path('flights/<int:pk>/detail', FlightDetailView.as_view(), name='flight_detail'),

    path('staff/', StaffCreateView.as_view(), name='staff_add'),
    path('staff/list', StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/update', StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete', StaffDeleteView.as_view(), name='staff_delete'),

    path('cities/', CityCreateView.as_view(), name='city_add'),
    path('cities/list', CitiesListView.as_view(), name='cities_list'),
    path('cities/list/filter', CitiesFilterView.as_view(), name='cities_filter'),
    path('cities/<int:pk>/detail', CityDetailView.as_view(), name='city_detail'),
    path('cities/<int:pk>/airports', AirportCreateView.as_view(), name='airport_add'),
    path('cities/<int:pk>/delete', CityDeleteView.as_view(), name='city_delete'),

    path('airplane/', AirplaneCreateView.as_view(), name='airplane_add'),
    path('airplane/list', AirplaneListView.as_view(), name='airplane_list'),
    path('airplane/<int:pk>/update', AirplaneUpdateView.as_view(), name='airplane_update'),
    path('airplane/<int:pk>/delete', AirplaneDeleteView.as_view(), name='airplane_delete'),

    path('discount/', DiscountCreateView.as_view(), name='discount_add'),
    path('discount/list', DiscountListView.as_view(), name='discount_list'),
    path('discount/<int:pk>/update', DiscountUpdateView.as_view(), name='discount_update'),
    path('discount/<int:pk>/delete', DiscountDeleteView.as_view(), name='discount_delete'),
]
