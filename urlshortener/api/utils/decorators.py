from functools import wraps
from flask import g, request, current_app
from jwt.exceptions import InvalidTokenError
from urlshortener.infrastructure.db.repositories.user import UserRepository
from urlshortener.infrastructure.db.repositories.url import UrlRepository
from urlshortener.infrastructure.cache.repositories.user import UserCache
from urlshortener.infrastructure.cache.repositories.url import UrlCache
from urlshortener.application.services import UserService, UrlService
from urlshortener.application.ports import TokenProvider


def inject_user_service(f):
    @wraps(f)
    def user_service_wrapper(*args, **kwargs):
        if current_app.config.get('REDIS_SETTINGS'):
            redis_config = current_app.config.get('REDIS_SETTINGS')
            user_service = UserService(
                password_hasher=current_app.config.get('PASSWORD_HASHER'),
                token_provider=current_app.config.get('TOKEN_PROVIDER'),
                repository=UserRepository(),
                cache=UserCache(**redis_config)
            )
        else:
            user_service = UserService(
                password_hasher=current_app.config.get('PASSWORD_HASHER'),
                token_provider=current_app.config.get('TOKEN_PROVIDER'),
                repository=UserRepository()
            )
            
        g.user_service = user_service
        return f(*args, **kwargs)

    return user_service_wrapper


def inject_url_service(f):
    @wraps(f)
    def url_service_wrapper(*args, **kwargs):
        if current_app.config.get('REDIS_SETTINGS'):
            redis_config = current_app.config.get('REDIS_SETTINGS')
            url_service = UrlService(
                url_normalizer=current_app.config.get('URL_NORMALIZER'),
                url_shortener=current_app.config.get('URL_SHORTENER'),
                repository=UrlRepository(),
                cache=UrlCache(**redis_config)
            )
        else:
            url_service = UrlService(
                url_normalizer=current_app.config.get('URL_NORMALIZER'),
                url_shortener=current_app.config.get('URL_SHORTENER'),
                repository=UrlRepository()
            )
        
        g.url_service = url_service
        return f(*args, **kwargs)

    return url_service_wrapper


def login_required(f):
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
            token_provider: TokenProvider = current_app.config.get(
                'TOKEN_PROVIDER'
            )
            payload = token_provider.get_token_payload(
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
