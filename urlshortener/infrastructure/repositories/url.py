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
            url_db = URL(
                original_url=url.original_url,
                short_url=url.url_key,
                user=url.user_id,
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
                user_id=url_db.user.id,
                created_at=url_db.created_at
            )
        else:
            return None

    def _get_url_by_user_origin(
        self,
        user_id: str,
        original_url: str
    ) -> Optional[URL]:
        url_db: URLDB = URLDB.objects(
            original_url=original_url,
            user_id=user_id
        ).first()
        if url_db:
            return url_factory(
                short_url=url_db.short_url,
                original_url=url_db.original_url,
                user_id=url_db.user.id,
                created_at=url_db.created_at
            )
        else:
            return None
