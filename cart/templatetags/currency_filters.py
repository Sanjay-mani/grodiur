from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    if value is None:
        return ''
    try:
        # Convert to string and then to Decimal safely
        dec_val = Decimal(str(value))
        # Quantize to 2 decimal places (standard mathematical rounding)
        dec_val = dec_val.quantize(Decimal('0.01'))
        # If it has no fractional part, display as integer
        if dec_val % 1 == 0:
            return f"{int(dec_val)}"
        else:
            # Show exactly 2 decimal places
            return f"{dec_val:.2f}"
    except (ValueError, TypeError, InvalidOperation):
        return value
