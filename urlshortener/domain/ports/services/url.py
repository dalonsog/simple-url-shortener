from abc import ABC, abstractmethod
from typing import Optional

from domain.model.url import URL, CreateUrlDto


class UrlServiceInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError
    
    def create(self, user: CreateUrlDto) -> Optional[URL]:
        return self._create(user)
    
    def get_url_by_key(self, url_key: str) -> Optional[URL]:
        return self._get_url_by_key(url_key)
    
    @abstractmethod
    def _create(self, user: CreateUrlDto) -> Optional[URL]:
        raise NotImplementedError
    
    @abstractmethod
    def _get_url_by_key(self, url_key: str) -> Optional[URL]:
        raise NotImplementedError
