from functools import wraps
from flask import g, request
from api.utils.auth import get_token_payload, InvalidTokenError


def login_required():
    def validate_token(f):
        @wraps(f)
        def func_wrapper(*args, **kwargs):
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
                payload = get_token_payload(token)
                g.current_user = payload
            except InvalidTokenError:
                return {
                    'error': 'Authorization error',
                    'data': "Token expired"
                }, 401

            return f(*args, **kwargs)

        return func_wrapper

    return validate_token
