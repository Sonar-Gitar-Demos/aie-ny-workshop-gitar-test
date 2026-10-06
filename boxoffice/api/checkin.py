from flask import Blueprint, request

from boxoffice import checkin
from boxoffice.api import now, store
from boxoffice.auth import require_staff

bp = Blueprint("checkin", __name__)


@bp.post("/events/<event_id>/scan")
@require_staff
def scan(event_id: str):
    body = request.get_json(silent=True) or {}
    code = str(body.get("code", "")).strip()
    ticket = checkin.scan(store(), code, event_id, now())
    return {"ticket_id": ticket.id, "checked_in_at": ticket.checked_in_at.isoformat()}
