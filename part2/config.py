import os


class Config:
    """Base configuration for the secret key and debug"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "default_secret_key"
    DEBUG = False


class DevelopmentConfig(Config):
    """Configuration for the development environment"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration for the environment"""
    TESTING = True
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
