import json
import os
import time
from datetime import datetime, timedelta

CACHE_DIR = 'cache'
CACHE_EXPIRY = 3600  # 1 hour in seconds

def ensure_cache_dir():
    """Ensure cache directory exists"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def get_cache_key(function_name, *args):
    """Generate cache key from function name and arguments"""
    key_parts = [function_name] + [str(arg) for arg in args]
    return '_'.join(key_parts).replace('/', '_').replace(':', '_').replace(' ', '_')[:200]

def get_cached_data(cache_key):
    """Retrieve cached data if it exists and is not expired"""
    ensure_cache_dir()
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)
                
            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time < timedelta(seconds=CACHE_EXPIRY):
                return cached['data']
        except Exception as e:
            print(f"Cache read error: {e}")
    
    return None

def set_cached_data(cache_key, data):
    """Store data in cache"""
    ensure_cache_dir()
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    try:
        cached = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        with open(cache_file, 'w') as f:
            json.dump(cached, f)
    except Exception as e:
        print(f"Cache write error: {e}")

def cached_function(func):
    """Decorator to add caching to a function"""
    def wrapper(*args, **kwargs):
        # Create cache key from function name and arguments
        cache_key = get_cache_key(func.__name__, *args)
        
        # Try to get cached data
        cached = get_cached_data(cache_key)
        if cached is not None:
            print(f"Cache hit for {func.__name__}")
            return cached
        
        # Execute function and cache result
        result = func(*args, **kwargs)
        set_cached_data(cache_key, result)
        
        return result
    
    return wrapper
