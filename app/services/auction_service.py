"""
Auction business logic service.
Contains the core auction functionality and business rules.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from ..models import Lot, Bid
from ..schemas import LotCreate, BidCreate, WebSocketMessage
from ..websocket_manager import manager


class AuctionService:
    """Service class for auction-related business logic."""
    
    @staticmethod
    def create_lot(db: Session, lot_data: LotCreate) -> Lot:
        """Create a new auction lot."""
        end_time = datetime.utcnow() + timedelta(minutes=lot_data.duration_minutes)
        
        db_lot = Lot(
            title=lot_data.title,
            description=lot_data.description,
            starting_price=lot_data.starting_price,
            current_price=lot_data.starting_price,
            end_time=end_time
        )
        
        db.add(db_lot)
        db.commit()
        db.refresh(db_lot)
        
        return db_lot
    
    @staticmethod
    def get_active_lots(db: Session) -> list[Lot]:
        """Get all active auction lots."""
        return db.query(Lot).filter(Lot.status == "running").all()
    
    @staticmethod
    def place_bid(db: Session, lot_id: int, bid_data: BidCreate) -> Bid:
        """Place a bid on an auction lot."""
        lot = db.query(Lot).filter(Lot.id == lot_id).first()
        if not lot:
            raise ValueError("Lot not found")
        
        if lot.status != "running":
            raise ValueError("Lot is not active")
        
        if datetime.utcnow() > lot.end_time:
            lot.status = "ended"
            db.commit()
            raise ValueError("Lot has ended")
        
        if bid_data.amount <= lot.current_price:
            raise ValueError("Bid must be higher than current price")
        
        db_bid = Bid(
            lot_id=lot_id,
            bidder=bid_data.bidder,
            amount=bid_data.amount
        )
        
        db.add(db_bid)
        
        lot.current_price = bid_data.amount
        
        if lot.end_time - datetime.utcnow() <= timedelta(minutes=5):
            lot.end_time = datetime.utcnow() + timedelta(minutes=5)
        
        db.commit()
        db.refresh(db_bid)
        
        return db_bid
    
    @staticmethod
    async def broadcast_bid_update(lot_id: int, bidder: str, amount: float):
        """Broadcast bid update to WebSocket clients."""
        message = WebSocketMessage(
            type="bid_placed",
            lot_id=lot_id,
            bidder=bidder,
            amount=amount
        )
        
        await manager.broadcast_to_lot(message.json(), lot_id)
