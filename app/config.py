import os
from typing import List, Type, Optional, ClassVar
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "NMAR Project"
    CONFIG_NAME: str = "base"
    DEBUG: bool = False
    DATABASE_URI: str = os.getenv("DATABASE_URI","mysql+pymysql://sai:sai@localhost:3306/test")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10  # 10 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES : int= 60 * 24 * 7  # 7 days
    ALGORITHM : str = "HS256"
    JWT_SECRET_KEY : str = os.environ.get('JWT_SECRET_KEY', "abcd")  # should be kept secret
    JWT_REFRESH_SECRET_KEY : str = os.environ.get('JWT_REFRESH_SECRET_KEY', "abcd1234")  # should be kept secret


class DevelopmentConfig(Settings):
    CONFIG_NAME: str = "dev"
    # add addition


class TestingConfig(Settings):
    CONFIG_NAME: str = "test"


class ProductionConfig(Settings):
    CONFIG_NAME: str = "prod"


def get_config(config):
    return config_by_name[config]


EXPORT_CONFIGS: List[Type[Settings]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg().CONFIG_NAME: cfg() for cfg in EXPORT_CONFIGS}
