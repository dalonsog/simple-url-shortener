import pytest
from urlshortener.domain.model.user import User
from urlshortener.domain.ports.repositories.user import UserRepositoryInterface
from urlshortener.domain.ports.repositories.exceptions import (
    UserDBOperationError
)


def test_get_user_not_found(fake_user_repository: UserRepositoryInterface):
    user_in_db = fake_user_repository.get_user_by_email('something@domain.com')
    assert user_in_db == None


def test_add_valid_user(
    fake_user_repository: UserRepositoryInterface,
    fake_user_object: User
):
    fake_user_repository.add(fake_user_object)
    assert True


def test_get_user_in_db(
    fake_user_repository: UserRepositoryInterface,
    fake_user_object: User
):
    user_in_db = fake_user_repository.get_user_by_email(fake_user_object.email)
    assert user_in_db == fake_user_object


def test_add_duplicated_user(
    fake_user_repository: UserRepositoryInterface,
    fake_user_object: User
):
    with pytest.raises(UserDBOperationError):
        fake_user_repository.add(fake_user_object)
