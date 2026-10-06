import itertools
import secrets
from dataclasses import dataclass, field
from datetime import datetime

# Public page for a ticket. The customer app links here.
TICKET_PAGE_URL = "https://boxoffice.example/t/"


@dataclass
class Event:
    id: str
    name: str
    venue: str
    starts_at: datetime
    price_cents: int
    capacity: int


@dataclass
class Order:
    id: str
    event_id: str
    buyer_email: str
    total_cents: int
    payment_id: str
    status: str = "paid"  # "paid" or "cancelled"


@dataclass
class Ticket:
    id: str
    order_id: str
    event_id: str
    price_cents: int
    holder_email: str  # who gets in at the door
    qr_token: str
    status: str = "valid"  # "valid" or "void"
    checked_in_at: datetime | None = None


def new_qr_token() -> str:
    return secrets.token_urlsafe(16)


@dataclass
class Store:
    """In-memory data for one app instance."""

    events: dict[str, Event] = field(default_factory=dict)
    orders: dict[str, Order] = field(default_factory=dict)
    tickets: dict[str, Ticket] = field(default_factory=dict)
    _counters: dict[str, itertools.count] = field(default_factory=dict)

    def next_id(self, prefix: str) -> str:
        return f"{prefix}_{next(self._counters.setdefault(prefix, itertools.count(1)))}"

    def tickets_for_order(self, order_id: str) -> list[Ticket]:
        return [t for t in self.tickets.values() if t.order_id == order_id]

    def tickets_held_by(self, email: str) -> list[Ticket]:
        return [t for t in self.tickets.values() if t.holder_email == email]

    def ticket_by_qr(self, qr_token: str) -> Ticket | None:
        return next((t for t in self.tickets.values() if t.qr_token == qr_token), None)

    def tickets_sold(self, event_id: str) -> int:
        return sum(1 for t in self.tickets.values() if t.event_id == event_id and t.status == "valid")
