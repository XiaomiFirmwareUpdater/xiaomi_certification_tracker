from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'gcf'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    model = Column('model', String(), nullable=False)
    device = Column('device', String(), nullable=False)
    date = Column('date', String(), nullable=False)
    certification = Column('certification', String(), nullable=False)
