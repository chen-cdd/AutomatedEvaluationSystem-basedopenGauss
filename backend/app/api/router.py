from fastapi import APIRouter

from app.api import routes_dashboard, routes_health, routes_models, routes_tasks

api_router = APIRouter()
api_router.include_router(routes_health.router)
api_router.include_router(routes_models.router)
api_router.include_router(routes_tasks.router)
api_router.include_router(routes_dashboard.router)
