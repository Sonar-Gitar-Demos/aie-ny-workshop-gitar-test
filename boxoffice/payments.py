from dataclasses import dataclass, field


@dataclass
class FakePayments:
    """Stands in for the card processor. Records every call so tests can check amounts."""

    charges: list[tuple[str, str, int]] = field(default_factory=list)  # (payment_id, email, cents)
    refunds: list[tuple[str, int]] = field(default_factory=list)  # (payment_id, cents)

    def charge(self, email: str, amount_cents: int) -> str:
        payment_id = f"pay_{len(self.charges) + 1}"
        self.charges.append((payment_id, email, amount_cents))
        return payment_id

    def refund(self, payment_id: str, amount_cents: int) -> None:
        self.refunds.append((payment_id, amount_cents))
