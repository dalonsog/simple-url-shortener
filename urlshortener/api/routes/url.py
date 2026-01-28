from flask import (
    Blueprint,
    Response,
    jsonify,
    redirect,
    g,
    request,
    current_app
)
from urlshortener.aplication.services import UrlService
from urlshortener.domain.model.url import URL
from urlshortener.api.utils.decorators import inject_url_service, login_required


bp = Blueprint('api', __name__)


@bp.route('/')
def index() -> Response:
    return 'Hello world'


@bp.route('/<string:url>', methods=['GET'])
@inject_url_service
def redirect_url(url: str) -> Response:
    url_service: UrlService = g.url_service
    url_in_db: URL = url_service.retrieve_url_and_increment_count(url)
    if url_in_db:
        return redirect(url_in_db.original_url)
    else:
        return jsonify({'error': 'URL not found'}), 404


@bp.route('/shorten', methods=['POST'])
@login_required
@inject_url_service
def shorten_url() -> Response:
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'URL not found in request'}), 400

    user_email: str = g.current_user.get('user_email')
    url_service: UrlService = g.url_service
    try:
        url_in_db, created = url_service.shorten_url(original_url, user_email)
        return jsonify({
            'original_url': original_url,
            'short_url': (
                f'{current_app.config.get("DOMAIN_NAME")}/'
                f'{url_in_db.short_url}'
            )
        }), 201 if created else 200
    except Exception as err:
        return jsonify({'error': f'Error creating short url: {err}'}), 500


@bp.route('/inspect/<string:url>', methods=['GET'])
@inject_url_service
def inspect_url(url: str) -> Response:
    url_service: UrlService = g.url_service
    url_in_db: URL = url_service.get_url_by_key(url)
    if url_in_db:
        return jsonify(url_in_db)
    else:
        return jsonify({'error': 'URL not found'}), 404
