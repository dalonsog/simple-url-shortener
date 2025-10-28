from flask import Flask
from urlshortener.infrastructure.db import db
from urlshortener.api.config import Settings


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SECRET_KEY'] = Settings.SECRET_KEY
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": Settings.MONGO_DATABASE,
            "host": Settings.MONGO_HOST,
            "port": Settings.MONGO_PORT,
            "username": Settings.MONGO_USERNAME,
            "password": Settings.MONGO_PASSWORD
        }
    ]
    db.init_app(app)

    from urlshortener.api.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from urlshortener.api.routes.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/users')
    
    from urlshortener.api.routes.url import bp as url_bp
    app.register_blueprint(url_bp)

    return app
