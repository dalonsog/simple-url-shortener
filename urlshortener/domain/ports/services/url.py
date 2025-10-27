from abc import ABC, abstractmethod
from typing import Optional

from urlshortener.domain.model.url import URL, CreateUrlDto


class UrlServiceInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError
    
    def create(self, url: CreateUrlDto) -> Optional[URL]:
        return self._create(url)
    
    def get_url_by_key(self, url_key: str) -> Optional[URL]:
        return self._get_url_by_key(url_key)
    
    def get_url_by_user_origin(
        self,
        user_id: str,
        original_url: str
    ) -> Optional[URL]:
        return self._get_url_by_user_origin(user_id, original_url)
    
    @abstractmethod
    def _create(self, url: CreateUrlDto) -> Optional[URL]:
        raise NotImplementedError
    
    @abstractmethod
    def _get_url_by_key(self, url_key: str) -> Optional[URL]:
        raise NotImplementedError
    
    @abstractmethod
    def _get_url_by_user_origin(
        self,
        user_id: str,
        original_url: str
    ) -> Optional[URL]:
        raise NotImplementedError
