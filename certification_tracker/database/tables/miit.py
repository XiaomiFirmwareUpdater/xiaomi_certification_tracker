from sqlalchemy import Table, Column, Integer, String

from certification_tracker.database import metadata


def create_table(table):
    Table(table, metadata,
          Column('id', Integer(), primary_key=True, autoincrement=True),
          Column('device', String(), nullable=False),
          Column('model', String(), nullable=False),
          Column('category', String(), nullable=False),
          Column('date', String()),
          Column('certification', String(), nullable=False)
          )
