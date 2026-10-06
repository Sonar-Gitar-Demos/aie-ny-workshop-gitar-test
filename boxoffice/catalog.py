from datetime import datetime, timezone

from boxoffice.models import Event, Store


def seed(store: Store) -> None:
    """Load the venue's upcoming events."""
    for event in (
        Event(
            id="evt_jazz",
            name="Night Shift Jazz Trio",
            venue="Harbor Hall",
            starts_at=datetime(2026, 11, 14, 1, 0, tzinfo=timezone.utc),
            price_cents=5000,
            capacity=200,
        ),
        Event(
            id="evt_comedy",
            name="Open Mic Comedy",
            venue="Harbor Hall",
            starts_at=datetime(2026, 11, 21, 0, 30, tzinfo=timezone.utc),
            price_cents=2500,
            capacity=80,
        ),
    ):
        store.events[event.id] = event
