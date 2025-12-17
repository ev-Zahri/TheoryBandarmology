import math

def safe_float(value, default=0.0):
    """Safely convert value to float, handling NaN and Infinity"""
    if value is None:
        return default
    try:
        val = float(value)
        if math.isnan(val) or math.isinf(val):
            return default
        return val
    except (ValueError, TypeError):
        return default