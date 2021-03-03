from sqlalchemy import Table, Column, Integer, String

from certification_tracker.database import metadata


def create_table(table):
      Table(table, metadata,
            Column('id', Integer(), primary_key=True, autoincrement=True),
            Column('manufacturer', String(), nullable=False),
            Column('model', String(), nullable=False),
            Column('soc', String(), nullable=False),
            Column('type', String(), nullable=False),
            Column('certification', String(), nullable=False),
            Column('date', String(), nullable=False),
            Column('level', String(), nullable=False),
            Column('method', String(), nullable=True)
            )
