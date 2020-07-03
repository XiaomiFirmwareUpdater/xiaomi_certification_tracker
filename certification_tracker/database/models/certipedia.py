from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'certipedia'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    models = Column('models', String(), nullable=False)
    certification = Column('certification', String(), nullable=False)
    link = Column('link', String(), nullable=False)
