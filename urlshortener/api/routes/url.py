from flask import (
    Blueprint,
    Response,
    jsonify,
    redirect,
    g,
    request,
    current_app
)
from urlshortener.api.config import Settings
from urlshortener.api.services.url import UrlService
from urlshortener.domain.model.url import URL, CreateUrlDto, create_url_factory
from urlshortener.api.utils.decorators import inject_url_service, login_required


bp = Blueprint('api', __name__)


@bp.route('/')
def index() -> Response:
    return 'Hello world'


@bp.route('/<string:url>', methods=['GET'])
@inject_url_service
def redirect_url(url: str) -> Response:
    url_service: UrlService = g.url_service
    url_in_db: URL = url_service.get_url_by_key(url)
    if url_in_db:
        url_service.increment_url_count(url_in_db.short_url)
        current_app.logger.info(
            f'Redirecting to {url_in_db.original_url} - '
            f'Clicks: {url_in_db.clicks}'
        )
        return redirect(url_in_db.original_url)
    else:
        return 'URL not found', 404


@bp.route('/shorten', methods=['POST'])
@login_required
@inject_url_service
def shorten_url() -> Response:
    original_url = request.json.get('url')
    user_email: str = g.current_user.get('user_email')
    
    url_service: UrlService = g.url_service
    url_in_db: URL = url_service.get_url_by_user_origin(
        user_email,
        original_url
    )
    if not url_in_db:
        url_key = UrlService.get_short_url(original_url, user_email)
        while URL.objects(short_url=url_key):
            url_key = UrlService.get_short_url(original_url, user_email)
        new_url: CreateUrlDto = create_url_factory(
            short_url=url_key,
            original_url=original_url,
            user_email=user_email
        )
        try:
            url_service.create(new_url)
        except:
            return "Error creating short url", 500
    
    return jsonify({
        'original_url': original_url,
        'short_url': f'{Settings.DOMAIN_NAME}/{url_in_db.short_url}'
    }), 201


@bp.route('/inspect/<string:url>', methods=['GET'])
@inject_url_service
def inspect_url(url: str) -> Response:
    url_service: UrlService = g.url_service
    url_in_db: URL = url_service.get_url_by_key(url)
    if url_in_db:
        return jsonify(url_in_db)
    else:
        return 'URL not found', 404