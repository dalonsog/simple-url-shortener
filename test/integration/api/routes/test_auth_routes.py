import pytest
from flask.testing import FlaskClient


@pytest.mark.integration
def test_signup(flask_client: FlaskClient):
    user_data = {
        'email': 'user@domain.com',
        'password': 's0m3s3cr3tp4ss20rd!',
        'name': 'User'
    }
    response = flask_client.post(
        '/signup',
        json=user_data
    )
    assert response.status_code == 201
    assert response.json['email'] == user_data['email']
    assert response.json['name'] == user_data['name']
    assert not 'password' in response.json


@pytest.mark.integration
def test_signup_invalid_data(flask_client: FlaskClient):
    user_data = {
        'email': 'userATdomain.com',
        'password': 's0m3s3cr3tp4ss20rd!',
        'name': 'User'
    }
    response = flask_client.post(
        '/signup',
        json=user_data
    )
    assert response.status_code == 400
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )


@pytest.mark.integration
def test_signup_duplicated_email(flask_client: FlaskClient):
    user_data = {
        'email': 'user@domain.com',
        'password': 's0m3s3cr3tp4ss20rd!',
        'name': 'User'
    }
    response = flask_client.post(
        '/signup',
        json=user_data
    )
    assert response.status_code == 409
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )


@pytest.mark.integration
def test_login(flask_client: FlaskClient):
    user_data = {
        'username': 'user@domain.com',
        'password': 's0m3s3cr3tp4ss20rd!'
    }
    response = flask_client.post(
        '/login',
        data=user_data
    )
    assert response.status_code == 200
    assert (
        'token' in response.json
        and isinstance(response.json.get('token'), str)
        and len(response.json.get('token')) > 0
    )


@pytest.mark.integration
def test_login_wrong_password(flask_client: FlaskClient):
    user_data = {
        'username': 'user@domain.com',
        'password': 'wrongPassword'
    }
    response = flask_client.post(
        '/login',
        data=user_data
    )
    assert response.status_code == 401
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )


@pytest.mark.integration
def test_login_missing_password(flask_client: FlaskClient):
    user_data = {
        'username': 'user@domain.com'
    }
    response = flask_client.post(
        '/login',
        data=user_data
    )
    assert response.status_code == 400
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )
