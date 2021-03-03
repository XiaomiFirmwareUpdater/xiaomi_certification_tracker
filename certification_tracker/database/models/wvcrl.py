from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'wvcrl'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    manufacturer = Column('manufacturer', String(), nullable=False)
    model = Column('model', String(), nullable=False)
    soc = Column('soc', String(), nullable=False)
    type = Column('type', String(), nullable=False)
    certification = Column('certification', String(), nullable=False)
    date = Column('date', String(), nullable=False)
    level = Column('level', String(), nullable=False)
    method = Column('method', String(), nullable=True)
