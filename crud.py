from sqlalchemy import (
    and_,
    or_,
)
from models import *


def insert_settings():
    ins = settings.insert().values(
        base_url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
        api_key = "None",
        language = "ru",
    )
    conn = engine.connect()
    conn.execute(ins)
    conn.close()
    return "ok"


def select_settings():
    sel = settings.select().where(settings.c.id == 1)
    conn = engine.connect()
    data = conn.execute(sel).fetchone()
    conn.close()
    if data is not None:
        return dict(data)
    else:
        return None


def update_settings(type: str, value: str):
    if type == "api_key":
        upd = settings.update().where(settings.c.id == 1).values(
            api_key = value
        )
    elif type == "base_url":
        upd = settings.update().where(settings.c.id == 1).values(
            base_url = value
        )
    elif type == "language":
        upd = settings.update().where(settings.c.id == 1).values(
            language = value
        )
    conn = engine.connect()
    conn.execute(upd)
    conn.close()
    return "ok"


def reset_settings():
    upd = settings.update().where(settings.c.id == 1).values(
        base_url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
        api_key = "None",
        language = "ru",
    )
    conn = engine.connect()
    conn.execute(upd)
    conn.close()
    return "ok"
