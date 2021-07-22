import os
from . import get_env

basedir = os.path.abspath(os.path.dirname(__file__))


class EnvConfig(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = get_env('SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = get_env("SQLALCHEMY_TRACK_MODIFICATIONS")


class DevelopmentEnv(EnvConfig):
    """Configurations for Development."""
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True

class StagingEnv(EnvConfig):
    """Configurations for Staging."""
    DEBUG = True


class ProductionEnv(EnvConfig):
    """Configurations for Production."""
    ENV = 'production'
    DEBUG = False


app_env = {
    'development': DevelopmentEnv,
    'staging': StagingEnv,
    'production': ProductionEnv,
}
