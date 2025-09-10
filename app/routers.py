from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List

from .database import get_db
from .schemas import LotCreate, LotResponse, BidCreate, BidResponse
from .websocket_manager import manager
from .services.auction_service import AuctionService


router = APIRouter()

# REST API Endpoints
@router.post("/lots", response_model=LotResponse)
async def create_lot(lot: LotCreate, db: Session = Depends(get_db)):
    """Create a new auction lot."""
    return AuctionService.create_lot(db, lot)


@router.get("/lots", response_model=List[LotResponse])
async def get_lots(db: Session = Depends(get_db)):
    """Get list of active auction lots."""
    return AuctionService.get_active_lots(db)


@router.post("/lots/{lot_id}/bids", response_model=BidResponse)
async def place_bid(lot_id: int, bid: BidCreate, db: Session = Depends(get_db)):
    """Place a bid on an auction lot."""
    try:
        db_bid = AuctionService.place_bid(db, lot_id, bid)
        
        # Broadcast to WebSocket clients
        await AuctionService.broadcast_bid_update(lot_id, bid.bidder, bid.amount)
        
        return db_bid
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))


# WebSocket endpoint
@router.websocket("/ws/lots/{lot_id}")
async def websocket_endpoint(websocket: WebSocket, lot_id: int):
    """WebSocket endpoint for real-time lot updates."""
    await manager.connect(websocket, lot_id)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, lot_id)
