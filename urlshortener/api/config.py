import os


class Settings:
    DOMAIN_NAME = os.getenv('DOMAIN_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY')

    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
    MONGO_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
