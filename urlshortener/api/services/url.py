import string
import hashlib
from time import time
from typing import Optional
from urlshortener.domain.model.url import URL, CreateUrlDto, url_factory
from urlshortener.domain.ports.services.url import UrlServiceInterface
from urlshortener.domain.ports.repositories.url import UrlRepositoryInterface


_ALPHABET = string.digits + string.ascii_letters


class UrlService(UrlServiceInterface):
    def __init__(self, repository: UrlRepositoryInterface) -> None:
        super().__init__()
        self._repository = repository
    
    def _create(self, url: CreateUrlDto) -> Optional[URL]:
        new_url = url_factory(
            short_url=url.short_url,
            original_url=url.original_url,
            user_id=url.user_id
        )
        try:
            self._repository.add(new_url)
            return new_url
        except:
            raise
    
    def _get_url_by_key(self, url_key: str) -> Optional[URL]:
        return self._repository.get_url_by_key(url_key)
    
    def _get_url_by_user_origin(
        self,
        user_id: str,
        original_url: str
    ) -> Optional[URL]:
        return self._repository.get_url_by_user_origin(user_id, original_url)
    
    @staticmethod
    def get_short_url(original_url: str, username: str) -> str:
        digest = hashlib.md5((original_url + username).encode()).hexdigest()
        md5_int = int(digest, 16) + int(time())
        return UrlService.to_base62(md5_int)

    @staticmethod
    def to_base62(num: int, alphabet: str = _ALPHABET) -> str:
        base = len(alphabet)
        result = []
        while num > 0:
            num, rem = divmod(num, base)
            result.append(alphabet[rem])
        return "".join(reversed(result))[:6]
