from functools import wraps
from flask import g, request, current_app
from urlshortener.infrastructure.repositories.user import UserRepository
from urlshortener.infrastructure.repositories.url import UrlRepository
from urlshortener.api.services.user import UserService, InvalidTokenError
from urlshortener.api.services.url import UrlService


def inject_user_service(f):
    @wraps(f)
    def user_service_wrapper(*args, **kwargs):
        user_service = UserService(UserRepository())
        g.user_service = user_service
        return f(*args, **kwargs)

    return user_service_wrapper


def inject_url_service(f):
    @wraps(f)
    def url_service_wrapper(*args, **kwargs):
        url_service = UrlService(UrlRepository())
        g.url_service = url_service
        return f(*args, **kwargs)

    return url_service_wrapper


def login_required(f):
    @inject_user_service
    @wraps(f)
    def login_wrapper(*args, **kwargs):
        no_auth_error_data = (
            {
                'error': 'Authorization error',
                'data': "Not authenticated"
            },
            401
        )

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return no_auth_error_data
        
        token = auth_header[7:]
        if not token:
            return no_auth_error_data
        
        try:
            user_service: UserService = g.user_service
            payload = user_service.get_token_payload(
                token,
                current_app.secret_key
            )
            g.current_user = payload
        except InvalidTokenError:
            return {
                'error': 'Authorization error',
                'data': "Token expired"
            }, 401

        return f(*args, **kwargs)

    return login_wrapper
