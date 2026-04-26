from typing import Any


def get_cache_key(prefix: str, **kwargs: Any) -> str:
    """
    Build a cache key from a prefix and arbitrary key-value pairs.
    """
    parts = [prefix] + [f"{k}{v}" for k, v in kwargs.items()]
    return "_".join(parts)


def parse_search_query(q: str) -> list[str] | None:
    q = q.strip()
    # Prevent queries that are just wildcard charactrs, which could lead to expensive database ops
    if q in {"%", "_"}:
        return None

    return [token.lower() for token in q.split() if token.strip()]
