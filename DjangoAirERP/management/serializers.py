from rest_framework import serializers
from .models import Ticket

STATUS = (
    (False, "Not registered"),
    (True, "Registered"),
)


class TicketSerializer(serializers.ModelSerializer):
    reservation = serializers.SerializerMethodField()
    self_check_in = serializers.SerializerMethodField()
    check_in = serializers.SerializerMethodField()
    boarding = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ("id", "reservation", "self_check_in", "check_in", "boarding")

    def get_reservation(self, obj):
        return STATUS[obj.reservation][1]

    def get_self_check_in(self, obj):
        return STATUS[obj.self_check_in][1]

    def get_check_in(self, obj):
        return STATUS[obj.check_in][1]

    def get_boarding(self, obj):
        return STATUS[obj.boarding][1]
