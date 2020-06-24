from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'tkdn'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    model = Column('model', String(), nullable=False)
    certification = Column('certification', String(), nullable=False)
    reference = Column('reference', String(), nullable=False)
    date = Column('date', String(), nullable=False)
    link = Column('link', String(), nullable=False)
