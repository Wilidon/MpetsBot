import sys
from functools import lru_cache

import pickledb
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

    pickle: str

    bot1: str
    bot2: str
    bot3: str
    bot4: str
    bot5: str
    bot6: str

    bot_password: str

    api_key: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


def get_db():
    db = pickledb.load(get_settings().pickle, True)
    try:
        db.lgetall("user_tasks")
    except KeyError:
        db.lcreate("user_tasks")
    try:
        db.lgetall("club_tasks")
    except KeyError:
        db.lcreate("club_tasks")
    try:
        db.get("boss_start")
    except KeyError:
        db.get("boss_start")
    try:
        db.get("boss_end")
    except KeyError:
        db.get("boss_end")
    return db

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