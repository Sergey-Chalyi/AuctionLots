from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import APP_HOST, APP_PORT
from .database import create_tables
from .routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    create_tables()
    yield


app = FastAPI(
    title="Auction Service",
    description="A FastAPI-based auction service with WebSocket support for real-time bid updates",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)