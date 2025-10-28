from dataclasses import dataclass
from pydantic import BaseModel
from datetime import datetime, timezone
from urlshortener.domain.model.validators import validate_url, validate_email


@dataclass
class URL:
    short_url: str
    original_url: str
    clicks: int
    user_email: str
    created_at: datetime

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, URL):
            return False
        return self.short_url == other.short_url
    
    def __str__(self):
        return f'URL("{self.short_url}")'


class CreateUrlDto(BaseModel):
    short_url: str
    original_url: str
    user_email: str


def url_factory(
    short_url: str,
    original_url: str,
    user_email: str,
    clicks: int = 0,
    created_at: datetime = datetime.now(timezone.utc)
) -> URL:
    # data validation
    for field in [short_url, original_url, user_email]:
        if not field:
            raise ValueError(
                'Mandatory fields "short_url", "original_url" and '
                '"user_email" cannot be empty'
            )
    
    if len(short_url) > 6:
        raise ValueError('URL key cannot be longer than 6 characters')
    
    if len(original_url) > 200:
        raise ValueError('URL cannot be longer than 200 characters')
    
    if not validate_url(original_url):
        raise ValueError("Wrong original url format")
    
    if not validate_email(user_email):
        raise ValueError("Wrong email format")
    
    return URL(
        short_url=short_url,
        original_url=original_url,
        user_email=user_email,
        clicks=clicks,
        created_at=created_at
    )


def create_url_factory(
    short_url: str,
    original_url: str,
    user_email: str
) -> CreateUrlDto:
    return CreateUrlDto(
        short_url=short_url,
        original_url=original_url,
        user_email=user_email
    )