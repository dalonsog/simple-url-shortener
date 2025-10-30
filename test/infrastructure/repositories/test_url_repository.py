import pytest
from urlshortener.domain.model.url import URL
from urlshortener.domain.ports.repositories.url import UrlRepositoryInterface
from urlshortener.domain.ports.repositories.exceptions import (
    URLDBOperationError
)


def test_get_url_not_found(fake_url_repository: UrlRepositoryInterface):
    url_in_db = fake_url_repository.get_url_by_key('abcdef')
    assert url_in_db == None


def test_add_valid_url(
    fake_url_repository: UrlRepositoryInterface,
    fake_url_object: URL
):
    fake_url_repository.add(fake_url_object)
    assert True


def test_get_url_in_db(
    fake_url_repository: UrlRepositoryInterface,
    fake_url_object: URL
):
    url_in_db = fake_url_repository.get_url_by_key(fake_url_object.short_url)
    assert url_in_db == fake_url_object


def test_add_duplicated_url(
    fake_url_repository: UrlRepositoryInterface,
    fake_url_object: URL
):
    with pytest.raises(URLDBOperationError):
        fake_url_repository.add(fake_url_object)
