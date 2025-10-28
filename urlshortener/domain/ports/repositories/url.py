from abc import ABC, abstractmethod
from typing import Optional

from urlshortener.domain.model.url import URL


class UrlRepositoryInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError
    
    def add(self, url: URL) -> None:
        self._add(url)

    def get_url_by_key(self, url_key: str) -> Optional[URL]:
        self._get_url_by_key(url_key)

    def get_url_by_user_origin(
        self,
        user_email: str,
        original_url: str
    ) -> Optional[URL]:
        self._get_url_by_user_origin(user_email, original_url)

    def update_url(self, url_key: str, new_url_data: URL) -> None:
        self._update_url(url_key, new_url_data)

    @abstractmethod
    def _add(self, url: URL) -> None:
        return NotImplementedError
    
    @abstractmethod
    def _get_url_by_key(self, url_key: str) -> Optional[URL]:
        return NotImplementedError

    @abstractmethod
    def _get_url_by_user_origin(
        self,
        user_email: str,
        original_url: str
    ) -> Optional[URL]:
        return NotImplementedError
    
    @abstractmethod
    def _update_url(self, url_key: str, new_url_data: URL) -> None:
        return NotImplementedError
