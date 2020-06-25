from sqlalchemy import Table, Column, Integer, String

from certification_tracker.database import metadata


def create_table(table):
      Table(table, metadata,
            Column('id', Integer(), primary_key=True, autoincrement=True),
            Column('brand', String(), nullable=False),
            Column('model', String(), nullable=False),
            Column('description', String(), nullable=False)
            )
