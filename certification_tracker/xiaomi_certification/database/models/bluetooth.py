from sqlalchemy import Column, Integer, String

from certification_tracker.xiaomi_certification.database.models import Base


class Item(Base):
    __tablename__ = 'bluetooth'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    name = Column('name', String())
    items = Column('items', String())
    certification = Column('certification', String(), nullable=False)
    type = Column('type', String())
    date = Column('date', String(), nullable=False)
