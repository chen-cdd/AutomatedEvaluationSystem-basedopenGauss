from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import ModelRegistry
from app.schemas.models import ModelCreate, ModelRead

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=list[ModelRead])
def list_models(db: Session = Depends(get_db)) -> list[ModelRegistry]:
    return list(db.scalars(select(ModelRegistry).order_by(ModelRegistry.created_at.desc())).all())


@router.post("", response_model=ModelRead)
def create_model(payload: ModelCreate, db: Session = Depends(get_db)) -> ModelRegistry:
    model = ModelRegistry(**payload.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
