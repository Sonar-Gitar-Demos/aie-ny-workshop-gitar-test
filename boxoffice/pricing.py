from boxoffice.models import Event


def order_total_cents(event: Event, quantity: int) -> int:
    """Amount charged at checkout for `quantity` tickets to `event`."""
    return event.price_cents * quantity
