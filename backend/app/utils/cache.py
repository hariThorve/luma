import functools
import time
from typing import Any, Callable, Dict, Tuple

# Simple in-memory cache
cache_store: Dict[Tuple, Tuple[Any, float]] = {}

def cache(ttl: int = 3600):
    """
    Simple in-memory cache decorator with TTL (time-to-live) in seconds.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a cache key from the function name and arguments
            key = (func.__name__, str(args), str(kwargs))
            
            # Check if we have a cached result that hasn't expired
            if key in cache_store:
                result, timestamp = cache_store[key]
                if time.time() - timestamp < ttl:
                    return result
            
            # Call the function and cache the result
            result = await func(*args, **kwargs)
            cache_store[key] = (result, time.time())
            return result
        
        return wrapper
    
    return decorator 