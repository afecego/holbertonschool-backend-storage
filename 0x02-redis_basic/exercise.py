#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method
"""
import redis
import uuid
from typing import Union


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
