#!/usr/bin/env python3
"""
Simple test client to demonstrate the auction service functionality.
This script creates a lot, places bids, and shows WebSocket messages.
"""

import asyncio
import websockets
import json
import requests
import time
from datetime import datetime

API_BASE = "http://localhost:8000"
WS_BASE = "ws://localhost:8000"

print("=" * 50)
print("AUCTION SERVICE TEST CLIENT")
print("=" * 50)
print(f"API Base URL: {API_BASE}")
print(f"WebSocket Base URL: {WS_BASE}")
print("=" * 50)

async def test_websocket(lot_id):
    """Test WebSocket connection and display messages."""
    uri = f"{WS_BASE}/ws/lots/{lot_id}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket for lot {lot_id}")
            
            # Listen for messages for 30 seconds
            timeout = 30
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    print(f"WebSocket message: {data}")
                except asyncio.TimeoutError:
                    continue
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed")
                    break
                    
    except Exception as e:
        print(f"WebSocket error: {e}")

def test_rest_api():
    """Test REST API endpoints."""
    print("Testing REST API...")
    
    # Create a lot
    lot_data = {
        "title": "Test Guitar",
        "description": "A beautiful test guitar for auction",
        "starting_price": 100.0,
        "duration_minutes": 2  # Short duration for testing
    }
    
    response = requests.post(f"{API_BASE}/lots", json=lot_data)
    if response.status_code == 200:
        lot = response.json()
        print(f"Created lot: {lot}")
        lot_id = lot['id']
        
        # Get active lots
        response = requests.get(f"{API_BASE}/lots")
        if response.status_code == 200:
            lots = response.json()
            print(f"Active lots: {lots}")
        
        # Place some bids
        bids = [
            {"bidder": "Alice", "amount": 120.0},
            {"bidder": "Bob", "amount": 150.0},
            {"bidder": "Charlie", "amount": 180.0},
        ]
        
        for bid_data in bids:
            response = requests.post(f"{API_BASE}/lots/{lot_id}/bids", json=bid_data)
            if response.status_code == 200:
                bid = response.json()
                print(f"Placed bid: {bid}")
            else:
                print(f"Failed to place bid: {response.text}")
            time.sleep(1)  # Wait between bids
        
        return lot_id
    else:
        print(f"Failed to create lot: {response.text}")
        return None

async def main():
    """Main test function."""
    print("Starting auction service test...")
    print("Make sure the service is running with: docker-compose up")
    print()
    
    # Test REST API
    lot_id = test_rest_api()
    
    if lot_id:
        print(f"\nStarting WebSocket test for lot {lot_id}...")
        print("WebSocket will listen for 30 seconds...")
        
        # Test WebSocket in a separate task
        await test_websocket(lot_id)
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(main())
