import pytest
from flask.testing import FlaskClient


@pytest.fixture(scope='function')
def token(flask_client: FlaskClient) -> str:
    user_data = {
        'username': 'user@domain.com',
        'password': 's0m3s3cr3tp4ss20rd!'
    }
    login_response = flask_client.post('/login', data=user_data)
    return login_response.json.get('token')


@pytest.mark.integration
def test_home(flask_client: FlaskClient):
    response = flask_client.get('/')
    assert response.status_code == 200
    assert b'Hello world' in response.data


@pytest.mark.integration
def test_shorten_url(flask_client: FlaskClient, token: str):
    response = flask_client.post(
        '/shorten',
        json={'url': 'https://www.google.com/'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert (
        'original_url' in response.json
        and isinstance(response.json.get('original_url'), str)
        and len(response.json.get('original_url')) > 0
    )
    assert (
        'short_url' in response.json
        and isinstance(response.json.get('short_url'), str)
        and len(response.json.get('short_url')) > 0
    )


@pytest.mark.integration
def test_shorten_url_already_shortened_by_user(
    flask_client: FlaskClient,
    token: str
):
    first_response = flask_client.post(
        '/shorten',
        json={'url': 'https://www.google.com/'},
        headers={'Authorization': f'Bearer {token}'}
    )
    first_key = first_response.json.get('short_url')

    second_response = flask_client.post(
        '/shorten',
        json={'url': 'https://www.google.com/'},
        headers={'Authorization': f'Bearer {token}'}
    )
    second_key = second_response.json.get('short_url')

    assert second_response.status_code == 200
    assert second_key == first_key


@pytest.mark.integration
def test_shorten_url_bad_request(flask_client: FlaskClient, token: str):
    response = flask_client.post(
        '/shorten',
        json={'long_url': 'https://www.google.com/'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 400
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )


@pytest.mark.integration
def test_shorten_url_not_logged_in(flask_client: FlaskClient):
    response = flask_client.post(
        '/shorten',
        json={'url': 'https://www.google.com/'}
    )
    assert response.status_code == 401
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )


@pytest.mark.integration
def test_redirect_url(flask_client: FlaskClient, token:str):
    first_response = flask_client.post(
        '/shorten',
        json={'url': 'https://www.google.com/'},
        headers={'Authorization': f'Bearer {token}'}
    )
    short_url = first_response.json.get('short_url').split('/')[-1]
    
    response = flask_client.get(f'/{short_url}')
    assert response.status_code == 302


@pytest.mark.integration
def test_redirect_url_not_found(flask_client: FlaskClient):
    response = flask_client.get(f'/abcdef')
    assert response.status_code == 404
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )


@pytest.mark.integration
def test_inspect_url(flask_client: FlaskClient, token:str):
    first_response = flask_client.post(
        '/shorten',
        json={'url': 'https://www.google.com/'},
        headers={'Authorization': f'Bearer {token}'}
    )
    short_url = first_response.json.get('short_url').split('/')[-1]
    
    response = flask_client.get(f'/inspect/{short_url}')
    assert response.status_code == 200
    for field in ['original_url', 'short_url', 'user_email', 'created_at']:
        assert (
            field in response.json
            and isinstance(response.json.get(field), str)
            and len(response.json.get(field)) > 0
        )
    assert (
            'clicks' in response.json
            and isinstance(response.json.get('clicks'), int)
            and response.json.get('clicks') > 0
        )


@pytest.mark.integration
def test_inspect_url_not_found(flask_client: FlaskClient):
    response = flask_client.get(f'/inspect/abcdef')
    assert response.status_code == 404
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )

