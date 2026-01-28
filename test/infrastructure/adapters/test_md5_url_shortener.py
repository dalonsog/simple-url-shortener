import pytest
from urlshortener.application.ports import UrlShortener


@pytest.mark.unit
def test_get_short_url(md5_url_shortener: UrlShortener):
    url = 'https://www.google.com/'
    user = 'user'
    short_url = md5_url_shortener.get_short_url(url, user)

    assert type(short_url) == str
    assert len(short_url) == 6


@pytest.mark.unit
def test_same_url_twice(md5_url_shortener: UrlShortener):
    url = 'https://www.google.com/'
    user = 'user'
    short_url_1 = md5_url_shortener.get_short_url(url, user)
    short_url_2 = md5_url_shortener.get_short_url(url, user)

    assert short_url_1 != short_url_2


@pytest.mark.unit
def test_same_url_different_users(md5_url_shortener: UrlShortener):
    url = 'https://www.google.com/'
    user_1 = 'user1'
    user_2 = 'user2'
    short_url_1 = md5_url_shortener.get_short_url(url, user_1)
    short_url_2 = md5_url_shortener.get_short_url(url, user_2)

    assert short_url_1 != short_url_2
