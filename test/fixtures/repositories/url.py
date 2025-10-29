from typing import Optional
from urlshortener.domain.model.url import URL
from urlshortener.domain.ports.repositories.url import UrlRepositoryInterface
from urlshortener.domain.ports.repositories.exceptions import (
    URLDBOperationError
)


class FakeUrlRepository(UrlRepositoryInterface):
    def __init__(self) -> None:
        self._database: dict[str, URL] = {}
    
    def _add(self, url: URL) -> None:
        url_in_db = self.get_url_by_key(url.short_url)
        if url_in_db:
            raise URLDBOperationError(
                f'URL key {url.short_url} already exists'
            )
        
        self._database[url.short_url] = url
    
    def _get_url_by_key(self, url_key: str) -> Optional[URL]:
        return self._database.get(url_key)

    def _get_url_by_user_origin(
        self,
        user_email: str,
        original_url: str
    ) -> Optional[URL]:
        url_db = None
        for _, url in self._database.items():
            if (url.user_email == user_email
                and url.original_url == original_url
            ):
                url_db = {**url}
                break
        
        return url_db
        
    def _update_url(self, url_key: str, new_url_data: URL) -> None:
        url_in_db = self.get_url_by_key(url_key)
        if not url_in_db:
            raise URLDBOperationError(
                f'URL key {url_key} not found'
            )
        
        url_in_db.clicks = new_url_data.clicks
        self._database[url_key] = url_in_db
