#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method
"""
import redis
import uuid
from typing import Callable, Union, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """decorator that takes a single method Callable argument"""
    new_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Create and return function that increments the count for that key
        every time the method is called"""
        self._redis.incr(new_key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """decorator that takes a single method Callable argument"""
    in_data = method.__qualname__ + ":inputs"
    out_data = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args):
        """Create and return function that increments the count for that key
        every time the method is called"""
        self._redis.rpush(in_data, str(args))
        self._redis.rpush(out_data, method(self, *args))
        return method(self, *args)
    return wrapper


class Cache:
    def __init__(self):
        """store an instance of the Redis client as a private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """takes a data argument and returns a string"""
        key = str(uuid.uuid1())
        self._redis.mset({key: data})
        return (key)

    def get(self, key: str, fn: Optional[Callable] = None):
        """take a key string argument and an optional Callable argument
        named fn. callable will be used to convert the data back to the desired
        format"""
        desire = self._redis.get(key)
        if fn is not None:
            return fn(desire)
        return desire

    def get_str(self, data: str):
        """parametrize Cache.get with the correct conversion function."""
        return self.get(key, str)

    def get_int(self, data: int):
        """parametrize Cache.get with the correct conversion function."""
        return self.get(key, int)
