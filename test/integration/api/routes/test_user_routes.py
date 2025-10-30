import pytest
from flask.testing import FlaskClient


@pytest.mark.integration
def test_get_current_user(flask_client: FlaskClient):
    user_data = {
        'username': 'user@domain.com',
        'password': 's0m3s3cr3tp4ss20rd!'
    }
    login_response = flask_client.post('/login', data=user_data)
    token = login_response.json.get('token')
    
    response = flask_client.get(
        '/users/me',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert 'email' in response.json and 'name' in response.json
    assert response.json.get('email') == user_data.get('username')


@pytest.mark.integration
def test_get_current_user_not_logged_in(flask_client: FlaskClient):
    response = flask_client.get('/users/me')
    assert response.status_code == 401
    assert (
        'error' in response.json
        and isinstance(response.json.get('error'), str)
        and len(response.json.get('error')) > 0
    )
