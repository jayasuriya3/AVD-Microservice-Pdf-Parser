from decimal import Decimal


def calculate_overall(*values: Decimal) -> Decimal:
    if not values:
        return Decimal("0")
    return sum(values, Decimal("0")) / len(values)
