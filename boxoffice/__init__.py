"""Boxoffice: the ticketing API behind a small venue's website."""
from collections.abc import Callable
from datetime import datetime, timezone

from flask import Flask

from boxoffice import catalog
from boxoffice.api import checkin, events, orders, tickets
from boxoffice.errors import BoxofficeError
from boxoffice.models import Store
from boxoffice.payments import FakePayments


def create_app(clock: Callable[[], datetime] | None = None) -> Flask:
    app = Flask(__name__)
    app.config["CLOCK"] = clock or (lambda: datetime.now(timezone.utc))
    store = Store()
    catalog.seed(store)
    app.extensions["boxoffice.store"] = store
    app.extensions["boxoffice.payments"] = FakePayments()

    for module in (events, orders, tickets, checkin):
        app.register_blueprint(module.bp)

    @app.errorhandler(BoxofficeError)
    def refuse(err: BoxofficeError):
        return {"error": err.message}, err.status

    return app
