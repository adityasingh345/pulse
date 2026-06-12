from fastapi import FastAPI
from app.config import settings
from contextlib import asynccontextmanager
from app.database import engine
from app.api.endpoints.router import router as endpoints_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    print(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode")
    yield
    # Shutdown: runs when the app is stopping
    await engine.dispose()
    print("Database connections closed")

app = FastAPI(
    title = settings.APP_NAME,
    version="0.1.0",
    description="API reliability monitoring platform"
)

app.include_router(endpoints_router, prefix="/api/v1")

@app.get("/health", tags=["system"])
async def health():
    return {
        "status": "ok",
        "enviornment": settings.ENVIRONMENT,
        "version": "0.1.0",
    }