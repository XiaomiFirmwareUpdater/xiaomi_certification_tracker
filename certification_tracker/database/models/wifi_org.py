from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'wifi_org'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    device = Column('device', String(), nullable=False)
    model = Column('model', String(), nullable=False)
    category = Column('category', String(), nullable=False)
    date = Column('date', String(), nullable=False)
    certification = Column('certification', String(), nullable=False)
