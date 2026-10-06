from dataclasses import dataclass
from functools import wraps

from flask import g, request

from boxoffice.errors import BoxofficeError


@dataclass(frozen=True)
class Principal:
    email: str
    is_staff: bool = False


# Development stand-in for the identity service: bearer token -> principal.
DEV_TOKENS = {
    "tok_alice": Principal("alice@example.com"),
    "tok_bob": Principal("bob@example.com"),
    "tok_gate": Principal("gate@boxoffice.example", is_staff=True),
}


def _authenticate() -> Principal:
    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    principal = DEV_TOKENS.get(token)
    if principal is None:
        raise BoxofficeError("sign in required", 401)
    return principal


def require_customer(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        g.principal = _authenticate()
        return view(*args, **kwargs)

    return wrapper


def require_staff(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        g.principal = _authenticate()
        if not g.principal.is_staff:
            raise BoxofficeError("staff only", 403)
        return view(*args, **kwargs)

    return wrapper
