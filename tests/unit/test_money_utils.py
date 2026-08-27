from decimal import Decimal

from app.parsers.shared.money_utils import parse_decimal


def test_parse_decimal_preserves_exact_value() -> None:
    assert parse_decimal("₹1,234.50") == Decimal("1234.50")
