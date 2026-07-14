from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Session as ChatSession
from app.schemas import SessionCreate

router = APIRouter()
security = HTTPBearer()


def get_user(db: Session, token: str):

    user = db.query(User).filter(User.user_token == token).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


@router.post("/sessions")
def create_session(
    request: SessionCreate,
    # authorization: str = Header(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    # token = authorization.replace("Bearer ", "")
    token = credentials.credentials

    user = get_user(db, token)

    session = ChatSession(
        user_id=user.id,
        title=request.title or "New Chat"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


@router.get("/sessions")
def list_sessions(
    # authorization: str = Header(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    # token = authorization.replace("Bearer ", "")
    token = credentials.credentials

    user = get_user(db, token)

    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == user.id
    ).all()

    return sessions


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
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
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()

    return {"message": "Session deleted"}