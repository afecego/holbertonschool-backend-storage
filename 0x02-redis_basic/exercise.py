#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method
"""
import redis
import uuid
from typing import Callable, Union, Optional


class Cache:
    def __init__(self):
        """store an instance of the Redis client as a private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
