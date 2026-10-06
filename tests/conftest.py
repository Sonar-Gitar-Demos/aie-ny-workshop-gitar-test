from datetime import datetime, timedelta, timezone

import pytest

from boxoffice import create_app

from helpers import ALICE


class Clock:
    """A clock tests can move forward."""

    def __init__(self, now: datetime):
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **kwargs) -> None:
        self.now += timedelta(**kwargs)


@pytest.fixture
def clock():
    return Clock(datetime(2026, 10, 12, 16, 0, tzinfo=timezone.utc))


@pytest.fixture
def app(clock):
    return create_app(clock=clock)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def store(app):
    return app.extensions["boxoffice.store"]


@pytest.fixture
def payments(app):
    return app.extensions["boxoffice.payments"]


@pytest.fixture
def alice_order(client):
    """Alice buys two tickets to the jazz show."""
    resp = client.post("/orders", json={"event_id": "evt_jazz", "quantity": 2}, headers=ALICE)
    assert resp.status_code == 201
    return resp.get_json()

