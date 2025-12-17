from .safe_float import safe_float

def safe_int(value, default=0):
    """Safely convert value to int"""
    try:
        val = safe_float(value, default)
        return int(val) 
    except:
        return default