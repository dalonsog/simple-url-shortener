from datetime import datetime
from typing import Optional
from redis import Redis
from urlshortener.domain.model.user import User, user_factory
from urlshortener.domain.ports.repositories.user import UserRepositoryInterface
from urlshortener.infrastructure.cache import get_redis_client


class UserCache(UserRepositoryInterface):
    def __init__(self, host: str, port: int, password: str) -> None:
        self._cache: Redis = get_redis_client(host, port, password)
        self._prefix = 'user'
    
    def _add(self, user: User) -> None:
        user_in_cache = self.get_user_by_email(user.email)
        if not user_in_cache:
            self._cache.hset(
                f'{self._prefix}:{user.email}',
                mapping={
                    'name': user.name,
                    'password': user.password,
                    'created_at': int(user.created_at.timestamp())
                }
            )
    
    def _get_user_by_email(self, user_email: str) -> Optional[User]:
        user_in_cache: dict = self._cache.hgetall(
            f'{self._prefix}:{user_email}'
        )
        if user_in_cache:
            return user_factory(
                email=user_email,
                password=user_in_cache.get('password'),
                name=user_in_cache.get('name'),
                created_at=datetime.fromtimestamp(
                    int(user_in_cache.get('created_at'))
                )
            )
        else:
            return None
