from django.core.mail import send_mail
from django.template.loader import render_to_string
from DjangoAirERP.settings import EMAIL_HOST_USER
from management.models import Ticket


def send_tickets_by_mail(tickets_id, user):
    tickets = Ticket.objects.filter(id__in=tickets_id)
    send_mail(
        subject='Your weather',
        message="",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        html_message=render_to_string('email/registered_tickets.html',
                                      context={'tickets': tickets}),
    )
