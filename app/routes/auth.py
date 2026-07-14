from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models import User
from app.schemas import AuthResponse

router = APIRouter()


@router.post("/auth", response_model=AuthResponse)
def auth(db: Session = Depends(get_db)):

    token = str(uuid.uuid4())

    user = User(user_token=token)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user_token": token}