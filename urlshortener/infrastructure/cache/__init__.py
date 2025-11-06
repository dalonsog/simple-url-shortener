import os
from redis import Redis


def get_redis_client(host: str, port: int, password: str) -> Redis:
    return Redis(
        host=host,
        port=port,
        password=password,
        decode_responses=True,
        health_check_interval=5
    )
