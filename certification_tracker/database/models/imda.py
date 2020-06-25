from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'imda'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    brand = Column('brand', String(), nullable=False)
    model = Column('model', String(), nullable=False)
    description = Column('description', String(), nullable=False)
