from decimal import Decimal, ROUND_HALF_UP

def round_decimal(value):
    if value is None:
        return None
    return Decimal(value).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)