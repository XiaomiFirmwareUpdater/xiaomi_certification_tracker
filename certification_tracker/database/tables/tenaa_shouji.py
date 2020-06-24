from sqlalchemy import Table, Column, Integer, String

from certification_tracker.database import metadata


def create_table(table):
    Table(table, metadata,
          Column('id', Integer(), primary_key=True, autoincrement=True),
          Column('model', String(), nullable=False),
          Column('certification', String(), nullable=False),
          Column('photo', String())
          )
