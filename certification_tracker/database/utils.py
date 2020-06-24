from sqlalchemy import inspect

from certification_tracker.database import engine


def table_exists(table):
    ins = inspect(engine)
    return bool(table in ins.get_table_names())
