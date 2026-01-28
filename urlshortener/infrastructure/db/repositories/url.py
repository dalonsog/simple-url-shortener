from typing import Optional
from urlshortener.infrastructure.db.models.url import URLDB
from urlshortener.domain.model.url import URL, url_factory
from urlshortener.domain.ports.repositories.url import UrlRepositoryInterface
from urlshortener.domain.model.exceptions import (
    URLKeyAlreadyExistsException,
    URLKeyNotFoundException
)
from urlshortener.domain.ports.repositories.exceptions import (
    URLDBOperationError
)


class UrlRepository(UrlRepositoryInterface):
    def __init__(self) -> None:
        pass
    
    def add(self, url: URL) -> None:
        url_in_db = self.get_url_by_key(url_key=url.short_url)
        if url_in_db:
            raise URLKeyAlreadyExistsException(url_key=url.short_url)
        
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
    
    def get_url_by_key(self, url_key: str) -> Optional[URL]:
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

    def get_url_by_user_origin(
        self,
        user_email: str,
        original_url: str
    ) -> Optional[URL]:
        url_db: URLDB = URLDB.objects(
            user_email=user_email,
            original_url=original_url
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
        
    def update_url(self, url_key: str, new_url_data: URL) -> None:
        url_in_db: URLDB = URLDB.objects(short_url=url_key).first()
        if not url_in_db:
            raise URLKeyNotFoundException(url_key=url_key)
        
        url_in_db.clicks = new_url_data.clicks
        try:
            url_in_db.save()
        except Exception as excpt:
            raise URLDBOperationError(excpt)
