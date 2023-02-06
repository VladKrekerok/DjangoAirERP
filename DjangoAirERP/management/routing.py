from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/flights/<int:pk>', consumers.TicketConsumer.as_asgi())
]
