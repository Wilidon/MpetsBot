import sys
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str
    group_id: int
    tg_token: str

    db_host: str
    db_username: str
    db_password: str
    db_name: str

    chat_id: str

    bot1: str
    bot2: str
    bot3: str
    bot4: str
    bot5: str
    bot6: str

    bot_password: str
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


logger_config = {
    "handlers": [
        {"sink": sys.stdout},
        {"sink": "logs/main.log",
         "format": "{time} | {level} | {module}:{line}-- {message} - "
                   "{extra[""context]}",
         "rotation": "1 MB",
         "compression": "zip"},

    ],
    "extra": {"context": "None"}
}

logger_config_for_core = {
    "handlers": [
        {"sink": sys.stdout},
        {"sink": "logs/core.log",
         "format": "{time} | {level} | {module}:{line}-- {message} - "
                   "{extra[""context]}",
         "rotation": "1 MB",
         "compression": "zip"},

    ],
    "extra": {"context": "None"}
}