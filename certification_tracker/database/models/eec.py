from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'eec'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    brand = Column('brand', String())
    item = Column('item', String(), nullable=False)
    certification = Column('certification', String(), nullable=False)
    date = Column('date', String(), nullable=False)
