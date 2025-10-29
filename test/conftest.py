import pytest
from test.fixtures.repositories.url import FakeUrlRepository
from test.fixtures.repositories.user import FakeUserRepository


@pytest.fixture(scope='module')
def get_fake_url_repository() -> FakeUrlRepository:
    return FakeUrlRepository()


@pytest.fixture(scope='module')
def get_fake_user_repository() -> FakeUserRepository:
    return FakeUserRepository()
