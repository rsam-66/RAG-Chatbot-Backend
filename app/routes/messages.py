from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Session as ChatSession, Message

router = APIRouter()
security = HTTPBearer()


def get_user(db, token):

    user = db.query(User).filter(User.user_token == token).first()

    if not user:
        raise HTTPException(status_code=401)

    return user


@router.get("/sessions/{session_id}/messages")
def get_messages(
    session_id: int,
    limit: int = 20,
    # authorization: str = Header(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    # token = authorization.replace("Bearer ", "")
    token = credentials.credentials

    user = get_user(db, token)

    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404)

    messages = db.query(Message).filter(
        Message.session_id == session_id
    ).order_by(
        Message.created_at.desc()
    ).limit(limit).all()

    return messages[::-1]