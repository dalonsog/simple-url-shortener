import pytest
from datetime import datetime
from pydantic import ValidationError
from urlshortener.domain.model.url import (
    URL,
    CreateUrlDto,
    url_factory,
    create_url_factory
)


def test_create_url_valid_parameters():
    url = URL(
        short_url='kUjf3d',
        original_url='https://www.google.com/',
        clicks=0,
        user_email='user@domain.com',
        created_at=datetime.now()
    )
    assert isinstance(url, URL)


def test_create_url_missing_parameter():
    with pytest.raises(TypeError):
        URL(
            short_url='kUjf3d',
            original_url='https://www.google.com/',
            clicks=0,
            user_email='user@domain.com'
        )


def test_compare_two_equal_urls():
    url1 = URL(
        short_url='kUjf3d',
        original_url='https://www.google.com/',
        clicks=0,
        user_email='user@domain.com',
        created_at=datetime.now()
    )

    url2 = URL(
        short_url='kUjf3d',
        original_url='https://www.google.com/',
        clicks=0,
        user_email='user@domain.com',
        created_at=datetime.now()
    )

    assert url1 == url2


def test_compare_two_different_urls():
    url1 = URL(
        short_url='kUjf3d',
        original_url='https://www.google.com/',
        clicks=0,
        user_email='user@domain.com',
        created_at=datetime.now()
    )

    url2 = URL(
        short_url='1uHnf4',
        original_url='https://www.google.com/',
        clicks=0,
        user_email='user@domain.com',
        created_at=datetime.now()
    )

    assert url1 != url2
    

def test_string_representation():
    url = URL(
        short_url='kUjf3d',
        original_url='https://www.google.com/',
        clicks=0,
        user_email='user@domain.com',
        created_at=datetime.now()
    )

    assert str(url) == 'URL("kUjf3d")'


def test_create_url_with_factory_function():
    short_url='kUjf3d'
    original_url='https://www.google.com/'
    clicks=0
    user_email='user@domain.com'
    created_at=datetime.now()
    
    url = url_factory(
        short_url=short_url,
        original_url=original_url,
        clicks=clicks,
        user_email=user_email,
        created_at=created_at
    )
    
    assert isinstance(url, URL)
    assert url.short_url == short_url
    assert url.original_url == original_url
    assert url.clicks == clicks
    assert url.user_email == user_email
    assert url.created_at == created_at


def test_create_url_with_factory_function_missing_creation_time():
    short_url='kUjf3d'
    original_url='https://www.google.com/'
    clicks=0
    user_email='user@domain.com'
    created_at=datetime.now()
    
    url = url_factory(
        short_url=short_url,
        original_url=original_url,
        clicks=clicks,
        user_email=user_email,
        created_at=created_at
    )
    
    assert isinstance(url, URL)
    assert url.short_url == short_url
    assert url.original_url == original_url
    assert url.clicks == clicks
    assert url.user_email == user_email
    assert isinstance(url.created_at, datetime)


def test_create_url_with_factory_function_long_url_key():
    with pytest.raises(ValueError):
        url_factory(
            short_url='kUjf3d1u4',
            original_url='https://www.google.com/',
            clicks=0,
            user_email='user@domain.com',
            created_at=datetime.now()
        )


def test_create_user_with_factory_function_long_original_url():
    original_url = (
        'https://www.some.url.com/some/namespace/'
        'get-attribute-from-server-with-parameters?'
        'queryParam1=asjdsa&'
        'queryParam2=siudfyhsiudf&'
        'queryParam3=iuasydhausdhauysdhau&'
        'queryParam4=aushdausudanisudnjasda&'
        'queryParam5=asuydghauysdghauyshdua'
    )
    with pytest.raises(ValueError):
        url_factory(
            short_url='kUjf3d',
            original_url=original_url,
            clicks=0,
            user_email='user@domain.com',
            created_at=datetime.now()
        )


def test_create_url_with_factory_function_wrong_url():
    with pytest.raises(ValueError):
        url_factory(
            short_url='kUjf3d',
            original_url='httpj://www.go?ogle.com/',
            clicks=0,
            user_email='user@domain.com',
            created_at=datetime.now()
        )


def test_create_url_with_factory_function_wrong_email():
    with pytest.raises(ValueError):
        url_factory(
            short_url='kUjf3d',
            original_url='https://www.google.com/',
            clicks=0,
            user_email='userATdomain.com',
            created_at=datetime.now()
        )


def test_create_url_dto():
    data = {
        'short_url': 'kUjf3d',
        'original_url': 'https://www.google.com/',
        'user_email': 'userATdomain.com'
    }

    create_url = CreateUrlDto(**data)
    assert isinstance(create_url, CreateUrlDto)


def test_create_url_dto_with_factory():
    short_url='kUjf3d'
    original_url='https://www.google.com/'
    user_email='user@domain.com'

    create_url = create_url_factory(
        short_url=short_url,
        original_url=original_url,
        user_email=user_email
    )

    assert isinstance(create_url, CreateUrlDto)
    assert create_url.short_url == short_url
    assert create_url.original_url == original_url
    assert create_url.user_email == user_email
