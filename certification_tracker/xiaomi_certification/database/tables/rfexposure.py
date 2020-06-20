from sqlalchemy import Table, Column, Integer, String

from certification_tracker.xiaomi_certification.database import metadata


def create_table(table):
    Table(table, metadata,
          Column('id', Integer(), primary_key=True, autoincrement=True),
          Column('device', String(), nullable=False),
          Column('device_id', String(), nullable=False),
          Column('model', String(), nullable=False),
          Column('region', String(), nullable=False)
          )
