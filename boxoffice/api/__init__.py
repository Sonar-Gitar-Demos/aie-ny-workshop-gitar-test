"""HTTP layer. Route modules call these accessors instead of touching app state directly."""
from datetime import datetime

from flask import current_app

from boxoffice.models import Store
from boxoffice.payments import FakePayments


def store() -> Store:
    return current_app.extensions["boxoffice.store"]


def payments() -> FakePayments:
    return current_app.extensions["boxoffice.payments"]


def now() -> datetime:
    return current_app.config["CLOCK"]()
