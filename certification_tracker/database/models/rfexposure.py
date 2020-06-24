from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'rfexposure'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    device = Column('device', String(), nullable=False)
    device_id = Column('device_id', String(), nullable=False)
    model = Column('model', String(), nullable=False)
    region = Column('region', String(), nullable=False)
