from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str = Field(..., env='BOT_TOKEN')
    WEBAPP_URL: str = Field(..., env='WEBAPP_URL')

    class Config:
        env_file = ".env"


def load_config() -> Config:
    return Config()
