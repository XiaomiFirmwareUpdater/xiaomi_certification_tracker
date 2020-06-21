from sqlalchemy import Table, Column, Integer, String

from certification_tracker.xiaomi_certification.database import metadata


def create_table(table):
      Table(table, metadata,
            Column('id', Integer(), primary_key=True, autoincrement=True),
            Column('name', String()),
            Column('items', String()),
            Column('certification', String(), nullable=False),
            Column('type', String()),
            Column('date', String(), nullable=False)
            )
