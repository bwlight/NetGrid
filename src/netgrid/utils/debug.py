import time
from functools import wraps

def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        print(f"{fn.__name__} took {end - start:.4f}s")
        return result
    return wrapper

def trace(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"→ {fn.__name__} called")
        result = fn(*args, **kwargs)
        print(f"← {fn.__name__} returned {result}")
        return result
    return wrapper
