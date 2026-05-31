def mask_coordinate(value: float | None, precision: int = 4) -> float | None:
    if value is None:
        return None
    return round(float(value), precision)
