from django.db.models import QuerySet
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from .models import Ticket
from .serializers import TicketSerializer


class TicketConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    serializer_class = TicketSerializer

    def get_queryset(self, **kwargs) -> QuerySet:
        return Ticket.objects.filter(flight_id=self.scope['url_route']['kwargs']['pk']).order_by('id')

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Ticket)
    async def model_change(self, message, observer=None, **kwargs):
        if message['flight_id'] == self.scope['url_route']['kwargs']['pk']:
            await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        serializer = TicketSerializer(Ticket.objects.filter(flight_id=instance.flight.id).order_by('id'), many=True)
        return dict(data=serializer.data, action=action.value, flight_id=instance.flight.id)
