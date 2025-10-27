from flask import Blueprint, Response, request, jsonify
from api.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token
)
from api.models.url import User


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login() -> Response:
    user_email = request.form.get('username')
    user_pwd = request.form.get('password')
    if not user_email or not user_pwd:
        return 'Missing or incomplete user data', 400
    
    user: User = User.objects(email=user_email).first()
    if not user or not verify_password(user_pwd, user.password):
        return jsonify({'error': 'Wrong email/password combination'}), 400
    
    token = create_access_token({'email': user_email})

    return jsonify({'token': token})


@bp.route('/signup', methods=['POST'])
def signup() -> Response:
    user_data: dict = request.json
    try:
        new_user = User(**user_data)
        new_user.validate()
    except:
        return jsonify({'error': 'Missing or incomplete user data'}), 400

    if User.objects(email=new_user.email).first():
        return 'Input email already exists', 409
    
    new_user.password = get_password_hash(new_user.password)
    new_user.save()
    return jsonify({'email': new_user.email, 'name': new_user.name}), 201
