def section_confidence(found_fields: int, expected_fields: int) -> float:
    return found_fields / expected_fields if expected_fields else 0.0
