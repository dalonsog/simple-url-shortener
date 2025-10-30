import pytest
import mongomock
from flask import Flask
from urlshortener.domain.model.user import User, user_factory
from urlshortener.domain.model.url import URL, url_factory
from urlshortener.infrastructure.db import db
from urlshortener.infrastructure.repositories.user import UserRepository
from urlshortener.infrastructure.repositories.url import UrlRepository


def init_mock_db():
    app = Flask(__name__)

    app.config["MONGODB_SETTINGS"] = [
        {
            "db": 'mongoenginetest',
            "host": 'mongodb://localhost',
            "mongo_client_class": mongomock.MongoClient
        }
    ]
    db.init_app(app)


@pytest.fixture(scope='module')
def fake_url_repository() -> UrlRepository:
    init_mock_db()
    return UrlRepository()


@pytest.fixture(scope='module')
def fake_user_repository() -> UserRepository:
    init_mock_db()
    return UserRepository()


@pytest.fixture(scope='module')
def fake_user_object() -> User:
    return user_factory(
        email='user@domain.com',
        password='s0m3s3cr3tp4sssw0rd!',
        name='User'
    )


@pytest.fixture(scope='module')
def fake_url_object(fake_user_object: User) -> URL:
    return url_factory(
        short_url='kU4hnD',
        original_url='https://www.google.com/',
        user_email=fake_user_object.email
    )
