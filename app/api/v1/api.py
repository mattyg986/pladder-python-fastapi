from fastapi import APIRouter

from app.api.v1.endpoints import agents, health, agents_sdk

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(agents_sdk.router, prefix="/agents-sdk", tags=["agents-sdk"]) 