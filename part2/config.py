import os


class Config:
    """Base configuration for the secret key and debug"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"
    Debug = False


class DevelopmentConfig(Config):
    """Configuration for the development environment"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration for the environment"""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for the production environment"""
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
