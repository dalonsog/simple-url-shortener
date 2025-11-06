import pytest
import mongomock
from flask import Flask
from flask.testing import FlaskClient
from urlshortener.domain.model.user import User, user_factory
from urlshortener.domain.model.url import URL, url_factory
from urlshortener.infrastructure.db import db
from urlshortener.infrastructure.db.repositories.user import UserRepository
from urlshortener.infrastructure.db.repositories.url import UrlRepository
from urlshortener.api import register_routes


def init_mock_db(app: Flask):
    app.config["MONGODB_SETTINGS"] = [
        {
            "host": 'mongodb://localhost',
            "mongo_client_class": mongomock.MongoClient
        }
    ]
    db.init_app(app)


@pytest.fixture(scope='module')
def fake_url_repository() -> UrlRepository:
    init_mock_db(Flask('test-url-db'))
    return UrlRepository()


@pytest.fixture(scope='module')
def fake_user_repository() -> UserRepository:
    init_mock_db(Flask('test-user-db'))
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


@pytest.fixture(scope='module')
def flask_app() -> Flask:
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 's67dfgyuyufdsghfsyudhuihefrdkjfhuerjn'
    app.config['DOMAIN_NAME'] = 'http://127.0.0.1:5000'
    app.config['TESTING'] = True

    init_mock_db(app)
    
    register_routes(app)

    return app


@pytest.fixture(scope='module')
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()
