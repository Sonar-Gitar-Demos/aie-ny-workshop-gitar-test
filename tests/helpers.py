"""Shared test helpers: auth headers and API shortcuts."""

ALICE = {"Authorization": "Bearer tok_alice"}
BOB = {"Authorization": "Bearer tok_bob"}
GATE = {"Authorization": "Bearer tok_gate"}


def held_tickets(client, headers) -> list[dict]:
    return client.get("/me/tickets", headers=headers).get_json()["tickets"]


def scan(client, code: str, event_id: str = "evt_jazz"):
    return client.post(f"/events/{event_id}/scan", json={"code": code}, headers=GATE)
