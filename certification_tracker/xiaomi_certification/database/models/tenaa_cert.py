from sqlalchemy import Column, Integer, String

from certification_tracker.xiaomi_certification.database.models import Base


class Item(Base):
    __tablename__ = 'tenaa_cert'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    model = Column('model', String(), nullable=False)
    certification = Column('certification', String(), nullable=False)
    date = Column('date', String(), nullable=False)
    photos = Column('photos', String())
