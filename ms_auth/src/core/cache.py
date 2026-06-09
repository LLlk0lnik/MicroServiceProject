import json
from functools import wraps
from src.core.redis_client import get_redis


def async_cache(expire: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_parts = [func.__qualname__]
            for arg in args[1:]:
                key_parts.append(str(arg))
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}={v}")
            key = "cache:" + ":".join(key_parts)

            redis = await get_redis()
            cached = await redis.get(key)
            if cached is not None:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            if result is not None:
                await redis.setex(ket, expire, json.dumps(result, default=str))
            return result

        return wrapper

    return decorator
