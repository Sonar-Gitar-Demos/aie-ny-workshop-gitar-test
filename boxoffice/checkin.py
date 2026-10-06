from datetime import datetime

from boxoffice.errors import BoxofficeError
from boxoffice.models import Store, Ticket


class CheckinError(BoxofficeError):
    pass


def scan(store: Store, code: str, event_id: str, now: datetime) -> Ticket:
    """Admit the ticket whose QR code was scanned at a gate for `event_id`."""
    ticket = store.ticket_by_qr(code)
    if ticket is None:
        raise CheckinError("unknown ticket", 404)
    if ticket.event_id != event_id:
        raise CheckinError("ticket is for a different event", 409)
    if ticket.status != "valid":
        raise CheckinError("ticket is void", 409)
    if ticket.checked_in_at is not None:
        raise CheckinError("ticket already checked in", 409)
    ticket.checked_in_at = now
    return ticket
