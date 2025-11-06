from datetime import datetime
from typing import Optional
from redis import Redis
from urlshortener.domain.model.url import URL, url_factory
from urlshortener.domain.ports.repositories.url import UrlRepositoryInterface
from urlshortener.infrastructure.cache import get_redis_client


class UrlCache(UrlRepositoryInterface):
    def __init__(self, host: str, port: int, password: str) -> None:
        self._cache: Redis = get_redis_client(host, port, password)
        self._prefix = 'url'
    
    def _add(self, url: URL) -> None:
        url_in_cache = self.get_url_by_key(url.short_url)
        if not url_in_cache:
            self._cache.hset(
                f'{self._prefix}:{url.short_url}',
                mapping={
                    'original_url': url.original_url,
                    'user_email': url.user_email,
                    'clicks': url.clicks,
                    'created_at': int(url.created_at.timestamp())
                }
            )
    
    def _get_url_by_key(self, url_key: str) -> Optional[URL]:
        url_in_cache: dict = self._cache.hgetall(f'{self._prefix}:{url_key}')
        if url_in_cache:
            return url_factory(
                short_url=url_key,
                original_url=url_in_cache.get('original_url'),
                user_email=url_in_cache.get('user_email'),
                clicks=int(url_in_cache.get('clicks')),
                created_at=datetime.fromtimestamp(
                    int(url_in_cache.get('created_at'))
                )
            )
        else:
            return None

    def _get_url_by_user_origin(
        self,
        user_email: str,
        original_url: str
    ) -> Optional[URL]:
        return None
        
    def _update_url(self, url_key: str, new_url_data: URL) -> None:
        url_in_cache = self.get_url_by_key(url_key)
        if url_in_cache:
            self._cache.hset(
                f'{self._prefix}:{url_key}',
                mapping={
                    'original_url': new_url_data.original_url,
                    'user_email': new_url_data.user_email,
                    'clicks': new_url_data.clicks,
                    'created_at': int(new_url_data.created_at.timestamp())
                }
            )
