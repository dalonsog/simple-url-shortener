from typing import Optional
from urlshortener.domain.model.url import URL, url_factory
from urlshortener.domain.ports.repositories.url import UrlRepositoryInterface
from urlshortener.infrastructure.models.url import URLDB
from urlshortener.domain.ports.repositories.exceptions import (
    URLDBOperationError
)


class UrlRepository(UrlRepositoryInterface):
    def __init__(self) -> None:
        super().__init__()
    
    def _add(self, url: URL) -> None:
        url_in_db = self._get_url_by_key(url_key=url.short_url)
        if url_in_db:
            raise URLDBOperationError(
                f'URL key {url.short_url} already exists'
            )
        
        try:
            url_db = URLDB(
                original_url=url.original_url,
                short_url=url.short_url,
                user_email=url.user_email,
                clicks=0
            )
            url_db.save()
        except Exception as excpt:
            raise URLDBOperationError(excpt)
    
    def _get_url_by_key(self, url_key: str) -> Optional[URL]:
        url_db: URLDB = URLDB.objects(short_url=url_key).first()
        if url_db:
            return url_factory(
                short_url=url_db.short_url,
                original_url=url_db.original_url,
                user_email=url_db.user_email,
                clicks=url_db.clicks,
                created_at=url_db.created_at
            )
        else:
            return None

    def _get_url_by_user_origin(
        self,
        user_email: str,
        original_url: str
    ) -> Optional[URL]:
        url_db: URLDB = URLDB.objects(
            original_url=original_url,
            user_email=user_email
        ).first()
        if url_db:
            return url_factory(
                short_url=url_db.short_url,
                original_url=url_db.original_url,
                user_email=url_db.user_email,
                clicks=url_db.clicks,
                created_at=url_db.created_at
            )
        else:
            return None
        
    def _update_url(self, url_key: str, new_url_data: URL) -> None:
        url_in_db: URLDB = URLDB.objects(short_url=url_key).first()
        if not url_in_db:
            raise URLDBOperationError(
                f'URL key {url_key} not found'
            )
        
        url_in_db.clicks = new_url_data.clicks
        try:
            url_in_db.save()
        except Exception as excpt:
            raise URLDBOperationError(excpt)
