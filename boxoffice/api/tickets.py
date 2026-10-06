from flask import Blueprint, g

from boxoffice.api import store
from boxoffice.auth import require_customer
from boxoffice.models import TICKET_PAGE_URL, Ticket

bp = Blueprint("tickets", __name__)


def ticket_json(ticket: Ticket) -> dict:
    return {
        "id": ticket.id,
        "event_id": ticket.event_id,
        "status": ticket.status,
        "checked_in": ticket.checked_in_at is not None,
        "qr_token": ticket.qr_token,
        "ticket_url": TICKET_PAGE_URL + ticket.qr_token,
    }


@bp.get("/me/tickets")
@require_customer
def my_tickets():
    return {"tickets": [ticket_json(t) for t in store().tickets_held_by(g.principal.email)]}
