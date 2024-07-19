from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IOTEvent(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    device = Column(String)
    event_type = Column(String)
    event_data = Column(Float)
    timestamp = Column(DateTime)
