from flask import Blueprint, Response, jsonify, g
from api.utils.decorators import login_required
from api.models.url import User


bp = Blueprint('user', __name__)


@bp.route('/me', methods=['GET'])
@login_required()
def get_me() -> Response:
    current_user: dict = g.current_user
    current_user_data: User = User.objects(
        email=current_user.get('user_email')
    ).first()
    return jsonify({
        'email': current_user_data.email,
        'name': current_user_data.name
    })
