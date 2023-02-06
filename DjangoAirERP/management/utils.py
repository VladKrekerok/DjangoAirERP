from management.models import Ticket


def get_free_place(ticket):
    tickets = Ticket.objects.filter(flight=ticket.flight, place_type=ticket.place_type)
    all_places = range(1, len(tickets) + 1)
    places_taken = [ticket['place'] for ticket in tickets.exclude(place=None).values('place')]
    return list(set(all_places) - set(places_taken))[0]
