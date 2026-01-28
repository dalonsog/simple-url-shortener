import pytest
from jwt.exceptions import InvalidTokenError
from urlshortener.application.ports import TokenProvider


@pytest.mark.unit
def test_create_token(jwt_token_provider: TokenProvider):
    data = {
        'email': 'user1@email.com'
    }
    secret_key = '4sde5rf6tgyhuedrftygu'
    token = jwt_token_provider.create_access_token(data, secret_key)

    assert type(token) == str


@pytest.mark.unit
def test_get_token_payload(jwt_token_provider: TokenProvider):
    data = {
        'email': 'user1@email.com'
    }
    secret_key = '4sde5rf6tgyhuedrftygu'
    token = jwt_token_provider.create_access_token(data, secret_key)

    token_payload = jwt_token_provider.get_token_payload(token, secret_key)

    assert 'user_email' in token_payload
    assert token_payload.get('user_email') == data.get('email')


@pytest.mark.unit
def test_get_token_payload_wrong_token(jwt_token_provider: TokenProvider):
    data = {
        'email': 'user1@email.com'
    }
    secret_key = '4sde5rf6tgyhuedrftygu'
    token = jwt_token_provider.create_access_token(data, secret_key)

    with pytest.raises(InvalidTokenError):
        jwt_token_provider.get_token_payload(token + 'h', secret_key)
