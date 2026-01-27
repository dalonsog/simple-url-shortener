from abc import ABC, abstractmethod
from typing import Optional, Tuple
from urlshortener.domain.model.url import URL


class UrlServiceInterface(ABC):
    @abstractmethod
    def shorten_url(
        self,
        original_url: str,
        user_email: str
    ) -> Tuple[URL, bool]:
        raise NotImplementedError

    @abstractmethod
    def retrieve_url_and_increment_count(self, url_key: str) -> Optional[URL]:
        raise NotImplementedError
    
    @abstractmethod
    def get_url_by_key(self, url_key: str) -> Optional[URL]:
        raise NotImplementedError
