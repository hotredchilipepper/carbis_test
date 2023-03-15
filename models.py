# Описание моделей/таблиц БД

from sqlalchemy import MetaData
from database import engine
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
)

meta = MetaData()

settings = Table(
    "settings", meta,
    Column("id", Integer, primary_key=True),
    Column("base_url", String(256)),
    Column("api_key", String(64)),
    Column("language", String(4)),
)

meta.create_all(engine)
