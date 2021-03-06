from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    settings.db_username, settings.db_password,
    settings.db_host, settings.db_name)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
