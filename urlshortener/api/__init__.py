from flask import Flask
from urlshortener.infrastructure.db import db
from urlshortener.api.config import Settings


def register_routes(app: Flask) -> None:
    from urlshortener.api.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from urlshortener.api.routes.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/users')
    
    from urlshortener.api.routes.url import bp as url_bp
    app.register_blueprint(url_bp)


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SECRET_KEY'] = Settings.SECRET_KEY
    app.config['DOMAIN_NAME'] = Settings.DOMAIN_NAME
    app.config["MONGODB_SETTINGS"] = [
        {
            "host": Settings.MONGO_HOST,
            "port": Settings.MONGO_PORT,
            "username": Settings.MONGO_USERNAME,
            "password": Settings.MONGO_PASSWORD
        }
    ]
    app.config["REDIS_SETTINGS"] = {
        "host": Settings.REDIS_HOST,
        "port": Settings.REDIS_PORT,
        "password": Settings.REDIS_PASSWORD
    }
    
    db.init_app(app)

    register_routes(app)    

    return app
