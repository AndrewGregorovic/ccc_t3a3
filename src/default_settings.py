import os


def get_env_var(env_var):
    value = os.environ.get(env_var)

    if not value:
        raise ValueError(f"{env_var} is not set")

    return value


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "t3a3"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_env_var("DB_URI")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    @property
    def JWT_SECRET_KEY(self):
        return get_env_var("JWT_SECRET_KEY")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


environment = get_env_var("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
