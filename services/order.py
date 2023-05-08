from django.db import transaction

from db.models import User, Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: int = None
) -> Order:
    with transaction.atomic():
        if username:
            order = Order.objects.create(
                user=User.objects.get(username=username)
            )
        if date:
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            row = ticket_data["row"]
            seat = ticket_data["seat"]
            movie_session_id = ticket_data["movie_session"]
            Ticket.objects.create(
                row=row,
                seat=seat,
                movie_session_id=movie_session_id,
                order=order
            )
        return order


def get_orders(username: str = None) -> Order:
    with transaction.atomic():
        if username:
            return Order.objects.filter(user__username=username)
        else:
            return Order.objects.all().order_by("-user__username")