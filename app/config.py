import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LAPOSTE_BASE_URL = 'https://api.laposte.fr/suivi/v2/idships'
    LAPOSTE_API_KEY = os.environ.get('LAPOSTE_API_KEY')

class DevelopmentConfig(Config):
    ENV_TYPE = "development"


class ProductionConfig(Config):
    ENV_TYPE = "production"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
