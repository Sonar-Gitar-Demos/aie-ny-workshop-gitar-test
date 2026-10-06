from flask import Blueprint, g, request

from boxoffice import orders
from boxoffice.api import now, payments, store
from boxoffice.auth import require_customer
from boxoffice.models import Order

bp = Blueprint("orders", __name__)


def order_json(order: Order) -> dict:
    return {
        "id": order.id,
        "event_id": order.event_id,
        "total_cents": order.total_cents,
        "status": order.status,
        "ticket_ids": [t.id for t in store().tickets_for_order(order.id)],
    }


@bp.post("/orders")
@require_customer
def place_order():
    body = request.get_json(silent=True) or {}
    quantity = body.get("quantity")
    if not isinstance(quantity, int):
        raise orders.OrderError("quantity must be a whole number", 400)
    order = orders.place_order(store(), payments(), str(body.get("event_id", "")), g.principal.email, quantity, now())
    return order_json(order), 201


@bp.get("/orders/<order_id>")
@require_customer
def get_order(order_id: str):
    order = store().orders.get(order_id)
    if order is None or order.buyer_email != g.principal.email:
        raise orders.OrderError("order not found", 404)
    return order_json(order)


@bp.post("/orders/<order_id>/cancel")
@require_customer
def cancel_order(order_id: str):
    order = orders.cancel_order(store(), payments(), order_id, g.principal.email, now())
    return order_json(order)
