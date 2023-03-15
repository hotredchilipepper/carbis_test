# Подключение к БД.

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


SQLALCHEMY_DATABASE_URL = f"sqlite:///settingsDB.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, poolclass=NullPool
)
