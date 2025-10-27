from flask import (
    Blueprint,
    Response,
    jsonify,
    redirect,
    g,
    request,
    current_app
)
from api.config import Settings
from api.models.url import URL
from api.models.user import User
from api.utils.url import get_short_url
from api.utils.decorators import login_required


bp = Blueprint('api', __name__)


@bp.route('/')
def index() -> Response:
    return 'Hello world'


@bp.route('/<string:url>', methods=['GET'])
def redirect_url(url: str) -> Response:
    url: URL = URL.objects(short_url=url).first()
    if url:
        url.clicks += 1
        url.save()
        current_app.logger.info(
            f'Redirecting to {url.original_url} - Clicks: {url.clicks}'
        )
        return redirect(url.original_url)
    else:
        return 'URL not found', 404


@bp.route('/shorten', methods=['POST'])
@login_required()
def shorten_url() -> Response:
    original_url = request.json.get('url')
    user_email = g.current_user.get('user_email')
    user: User = User.objects(email=user_email).first()
    url_db: URL = URL.objects(original_url=original_url, user=user).first()
    if not url_db:
        url_key = get_short_url(original_url, username=user_email)
        while URL.objects(short_url=url_key):
            url_key = get_short_url(original_url, username=user_email)
        url_db = URL(
            original_url=original_url,
            short_url=url_key,
            user=user,
            clicks=0
        )
        url_db.save()
        current_app.logger.info(
            f'Created short url {url_key} for {original_url} by user {user_email}'
        )
    return jsonify({
        'original_url': original_url,
        'short_url': f'{Settings.DOMAIN_NAME}/{url_db.short_url}'
    }), 201


@bp.route('/inspect/<string:url>', methods=['GET'])
def inspect_url(url: str) -> Response:
    url: URL = URL.objects(short_url=url).first()
    if url:
        return jsonify(url)
    else:
        return 'URL not found', 404