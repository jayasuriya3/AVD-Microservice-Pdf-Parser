from decimal import Decimal, InvalidOperation


def parse_decimal(value: str) -> Decimal | None:
    cleaned = value.replace(",", "").replace("₹", "").strip()
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None
