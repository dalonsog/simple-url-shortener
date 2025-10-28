from flask import Blueprint, Response, jsonify, g
from urlshortener.domain.model.user import User
from urlshortener.api.services.user import UserService
from urlshortener.api.utils.decorators import login_required


bp = Blueprint('user', __name__)


@bp.route('/me', methods=['GET'])
@login_required
def get_me() -> Response:
    current_user: dict = g.current_user
    user_service: UserService = g.user_service
    current_user_data: User = user_service.get_user_by_email(
        current_user.get('user_email')
    )
    
    return jsonify({
        'email': current_user_data.email,
        'name': current_user_data.name
    })
