from typing import Any


def get_cache_key(prefix: str, **kwargs: Any) -> str:
    """
    Build a cache key from a prefix and arbitrary key-value pairs.
    """
    parts = [prefix] + [f"{k}{v}" for k, v in kwargs.items()]
    return "_".join(parts)
