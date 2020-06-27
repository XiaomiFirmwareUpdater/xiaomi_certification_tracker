from sqlalchemy import Column, Integer, String

from certification_tracker.database.models import Base


class Item(Base):
    __tablename__ = 'sirim'
    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    model = Column('model', String(), nullable=False)
    description = Column('description', String(), nullable=False)
    category = Column('category', String(), nullable=False)
    certification = Column('certification', String(), nullable=False)
    date = Column('date', String(), nullable=False)
