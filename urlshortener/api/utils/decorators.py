from flask import g, request
from urlshortener.infrastructure.repositories.user import UserRepository
from urlshortener.infrastructure.repositories.url import UrlRepository
from urlshortener.api.services.user import UserService, InvalidTokenError
from urlshortener.api.services.url import UrlService


def inject_user_service(f):
    def wrapper(*args, **kwargs):
        user_service = UserService(UserRepository())
        g.user_service = user_service
        return f(*args, **kwargs)

    return wrapper


def inject_url_service(f):
    def wrapper(*args, **kwargs):
        url_service = UrlService(UrlRepository())
        g.url_service = url_service
        return f(*args, **kwargs)

    return wrapper


def login_required(f):
    @inject_user_service
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return {
                'error': 'Authorization error',
                'data': "Not authenticated"
            }, 401
        
        token = auth_header[7:]

        if not token:
            return {
                'error': 'Authorization error',
                'data': "Not authenticated"
            }, 401
        
        try:
            user_service: UserService = g.user_service
            payload = user_service.get_token_payload(token)
            g.current_user = payload
        except InvalidTokenError:
            return {
                'error': 'Authorization error',
                'data': "Token expired"
            }, 401

        return f(*args, **kwargs)

    return wrapper
