from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'google_play'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    name = Column('name', String(), nullable=False)
    codename = Column('codename', String(), nullable=False)
    model = Column('model', String(), nullable=False)
