from typing import Optional, Tuple
from urlshortener.domain.model.url import URL, url_factory
from urlshortener.domain.ports.repositories.url import UrlRepositoryInterface
from urlshortener.domain.ports.services.url import UrlServiceInterface
from urlshortener.aplication.ports import UrlNormalizer, UrlShortener


class UrlService(UrlServiceInterface):
    def __init__(
        self,
        url_normalizer: UrlNormalizer,
        url_shortener: UrlShortener,
        repository: UrlRepositoryInterface,
        cache: Optional[UrlRepositoryInterface] = None,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._url_normalizer = url_normalizer
        self._url_shortener = url_shortener

    def shorten_url(
        self,
        original_url: str,
        user_email: str,
    ) -> Tuple[URL, bool]:
        normalized_url = self._url_normalizer.normalize_url(original_url)
        url_in_db = self._repository.get_url_by_user_origin(
            user_email,
            normalized_url
        )

        if url_in_db:
            return url_in_db, False
        
        url_key = self._url_shortener.get_short_url(normalized_url, user_email)
        while self.get_url_by_key(url_key):
            url_key = self._url_shortener.get_short_url(
                normalized_url,
                user_email
            )

        new_url = url_factory(
            short_url=url_key,
            original_url=normalized_url,
            user_email=user_email
        )

        try:
            self._repository.add(new_url)
            return new_url, True
        except:
            raise

    def retrieve_url_and_increment_count(self, url_key: str) -> Optional[URL]:
        current_url_data = self.get_url_by_key(url_key)
        if not current_url_data:
            return None
        
        current_url_data.clicks += 1
        try:
            self._repository.update_url(url_key, current_url_data)
            if self._cache:
                self._cache.update_url(url_key, current_url_data)
        except:
            raise

        return current_url_data
    
    def get_url_by_key(self, url_key: str) -> Optional[URL]:
        if not self._cache:            
            return self._repository.get_url_by_key(url_key)
        
        url_in_cache = self._cache.get_url_by_key(url_key)
        if url_in_cache:
            return url_in_cache
        
        url_in_db = self._repository.get_url_by_key(url_key)
        if url_in_db:
            self._cache.add(url_in_db)
        
        return url_in_db
