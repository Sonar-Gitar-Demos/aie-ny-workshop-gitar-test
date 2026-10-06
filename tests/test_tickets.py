from helpers import ALICE, BOB, held_tickets


def test_buyer_holds_the_tickets_they_bought(client, alice_order):
    tickets = held_tickets(client, ALICE)
    assert sorted(t["id"] for t in tickets) == sorted(alice_order["ticket_ids"])
    assert all(t["ticket_url"] == "https://boxoffice.example/t/" + t["qr_token"] for t in tickets)


def test_other_customers_do_not_see_them(client, alice_order):
    assert held_tickets(client, BOB) == []
