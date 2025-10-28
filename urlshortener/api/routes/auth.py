from flask import Blueprint, Response, request, jsonify, g
from urlshortener.domain.model.user import (
    User,
    RegisterUserInputDto,
    RegisterUserOutputDto,
    register_user_factory
)
from urlshortener.api.services.user import UserService
from urlshortener.api.utils.decorators import inject_user_service


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
@inject_user_service
def login() -> Response:
    user_email = request.form.get('username')
    user_pwd = request.form.get('password')
    if not user_email or not user_pwd:
        return 'Missing or incomplete user data', 400
    
    user_service: UserService = g.user_service
    user: User = user_service.get_user_by_email(user_email)
    if not user or not user_service.verify_password(user_pwd, user.password):
        return jsonify({'error': 'Wrong email/password combination'}), 400
    
    token = user_service.create_access_token({'email': user_email})

    return jsonify({'token': token})


@bp.route('/signup', methods=['POST'])
@inject_user_service
def signup() -> Response:
    user_data: dict = request.json
    user_service: UserService = g.user_service
    try:
        user_input: RegisterUserInputDto = register_user_factory(**user_data)
    except:
        return jsonify({'error': 'Missing or incomplete user data'}), 400

    try:
        new_user: RegisterUserOutputDto = user_service.create(user_input)
    except:
        return 'Input email already exists', 409
    
    return jsonify({'email': new_user.email, 'name': new_user.name}), 201
