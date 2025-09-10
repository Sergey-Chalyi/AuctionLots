# Auction Lots Service

A FastAPI-based auction service with WebSocket support for real-time bid updates.

## Features

- **REST API** for managing auction lots and placing bids
- **WebSocket** support for real-time bid notifications
- **PostgreSQL** database for data persistence
- **Docker** containerization for easy deployment
- **Automatic time extension** when bids are placed in the last 5 minutes

## API Endpoints

### REST Endpoints

- `POST /lots` - Create a new auction lot
- `GET /lots` - Get list of active lots
- `POST /lots/{lot_id}/bids` - Place a bid on a lot

### WebSocket

- `GET /ws/lots/{lot_id}` - Subscribe to real-time updates for a specific lot

## Message Format

WebSocket messages follow this format:

```json
{
  "type": "bid_placed",
  "lot_id": 1,
  "bidder": "John",
  "amount": 105
}
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system

### Environment Configuration

1. **Create environment file** (optional - defaults are provided):
   ```bash
   cp env.example .env
   ```

2. **Edit the .env file** with your preferred settings:
   ```bash
   # Database Configuration
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=auction_db
   DB_USER=postgres
   DB_PASSWORD=your_secure_password

   # Application Configuration
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DEBUG=True
   ```

### Launch the Application

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd AuctionLots
   ```

2. **Start the services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - API Documentation: http://localhost:8000/docs
   - WebSocket endpoint: ws://localhost:8000/ws/lots/{lot_id}
   - **Note**: The application runs on port 8000, not 5432 (which is the database port)


## Usage Examples

### Create a Lot

```bash
curl -X POST "http://localhost:8000/lots" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Vintage Guitar",
    "description": "Beautiful 1960s Fender Stratocaster",
    "starting_price": 1000.0,
    "duration_minutes": 60
  }'
```

### Place a Bid

```bash
curl -X POST "http://localhost:8000/lots/1/bids" \
  -H "Content-Type: application/json" \
  -d '{
    "bidder": "John",
    "amount": 1200.0
  }'
```

### Get Active Lots

```bash
curl -X GET "http://localhost:8000/lots"
```

## Database Schema

### Lots Table
- `id` - Primary key
- `title` - Lot title
- `description` - Lot description
- `starting_price` - Initial price
- `current_price` - Current highest bid
- `status` - "running" or "ended"
- `created_at` - Creation timestamp
- `end_time` - Auction end time

### Bids Table
- `id` - Primary key
- `lot_id` - Foreign key to lots
- `bidder` - Bidder name
- `amount` - Bid amount
- `placed_at` - Bid timestamp

## Auction Logic

- Lots start with a "running" status
- Bids must be higher than the current price
- If a bid is placed within the last 5 minutes, the auction is extended by 5 minutes
- Lots automatically end when the end time is reached
- All connected WebSocket clients receive real-time updates when bids are placed

## Security

### Environment Variables
- All sensitive configuration is stored in environment variables
- Never commit `.env` files to version control
- Use strong passwords for production databases
- The `env.example` file shows the required configuration without sensitive data


## Development

The application uses:
- **FastAPI** for the web framework
- **SQLAlchemy** for database ORM
- **PostgreSQL** for data storage
- **WebSockets** for real-time communication
- **Docker** for containerization
- **python-dotenv** for environment variable management

## Stopping the Application

To stop the application:

```bash
docker-compose down
```

To also remove the database volume:

```bash
docker-compose down -v
```