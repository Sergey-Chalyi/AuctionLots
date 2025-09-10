from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Lot(Base):
    __tablename__ = "lots"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    starting_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    status = Column(String, default="running")  # running, ended
    created_at = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)


class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(Integer, nullable=False)
    bidder = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    placed_at = Column(DateTime, default=datetime.utcnow)
