from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'mi_global'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    device = Column('device', String(), nullable=False)
    certification = Column('certification', String())
    region = Column('region', String(), nullable=False)
