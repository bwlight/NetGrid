def clamp(value, min_v, max_v):
    return max(min_v, min(value, max_v))

def percent(value, pct):
    return value * (pct / 100)

def safe_int(value):
    try:
        return int(value)
    except Exception:
        return 0
