from flask import Blueprint, Response, request, jsonify, g, current_app
from urlshortener.domain.model.user import (
    User,
    RegisterUserInputDto,
    RegisterUserOutputDto,
    register_user_factory
)
from urlshortener.aplication.services import UserService
from urlshortener.aplication.exception import NotAuthorizedException
from urlshortener.api.utils.decorators import inject_user_service


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
@inject_user_service
def login() -> Response:
    user_email = request.form.get('username')
    user_pwd = request.form.get('password')
    if not user_email or not user_pwd:
        return jsonify({'error': 'Missing or incomplete user data'}), 400
    
    user_service: UserService = g.user_service
    try:
        token = user_service.login_user(
            user_email=user_email,
            user_pwd=user_pwd,
            secret_key=current_app.secret_key
        )
        return jsonify({'token': token})
    except NotAuthorizedException:
        return jsonify({'error': 'Wrong email/password combination'}), 401
    

@bp.route('/signup', methods=['POST'])
@inject_user_service
def signup() -> Response:
    user_data: dict = request.json
    try:
        user_input: RegisterUserInputDto = register_user_factory(**user_data)
    except:
        return jsonify({'error': 'Missing or incomplete user data'}), 400

    user_service: UserService = g.user_service
    try:
        new_user: RegisterUserOutputDto = user_service.create_user(user_input)
    except Exception:
        return jsonify({'error': 'Input email already exists'}), 409
    
    return jsonify({'email': new_user.email, 'name': new_user.name}), 201
