# <----- ----->
from app.database import Base, get_db, engine
from app.models import Message, Session as ChatSession, User
from sqlalchemy.orm import Session
from fastapi import Depends, Header
from app.routes import auth, sessions, messages, data
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# <----- ----->
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from app.chatbot import RAGChatbot
from app.initialize import initialize_vectorstore
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chatbot API", version="1.0")

# <----- ----->
app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(messages.router)
app.include_router(data.router)
Base.metadata.create_all(bind=engine)
security = HTTPBearer()
# <----- ----->

chatbot = None


@app.on_event("startup")
def startup_event():
    global chatbot
    try:
        logger.info("Starting vector store initialization at startup...")
        initialize_vectorstore(force_rebuild=False)
        logger.info("Vector store initialized at startup")
        
        logger.info("Initializing RAG chatbot at startup...")
        chatbot = RAGChatbot()
        logger.info("RAG chatbot initialized at startup successfully")
    except Exception as e:
        logger.error(f"Startup initialization error: {str(e)}", exc_info=True)


class QueryRequest(BaseModel):
    question: str


class InitializeRequest(BaseModel):
    force_rebuild: bool = False


@app.post("/initialize")
def initialize(request: InitializeRequest, background_tasks: BackgroundTasks):

    def run_initialization():
        global chatbot
        try:
            logger.info("Starting vector store initialization...")
            initialize_vectorstore(force_rebuild=request.force_rebuild)
            logger.info("Vector store initialized successfully")
            
            logger.info("Initializing RAG chatbot...")
            chatbot = RAGChatbot()
            logger.info("RAG chatbot initialized successfully")
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}", exc_info=True)

    background_tasks.add_task(run_initialization)

    return {
        "message": "Initialization started in background",
        "force_rebuild": request.force_rebuild
    }


@app.post("/chat")
def chat(request: QueryRequest):

    if chatbot is None:
        return {"error": "Vector database not initialized yet"}

    response = chatbot.ask(request.question)
    return response


@app.get("/")
def root():
    return {"message": "RAG Chatbot API is running"}

# <----- ----->
def build_history(messages):

    history_lines = []

    for msg in messages:
        if msg.role == "user":
            history_lines.append(f"User: {msg.content}")
        else:
            history_lines.append(f"Assistant: {msg.content}")

    return "\n".join(history_lines)

@app.post("/sessions/{session_id}/chat")
def chat_session(
    session_id: int,
    request: QueryRequest,
    # authorization: str = Header(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    if chatbot is None:
        return {"error": "Vector database not initialized yet"}

    token = credentials.credentials

    user = db.query(User).filter(User.user_token == token).first()

    if not user:
        return {"error": "Invalid token"}

    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user.id
    ).first()

    if not session:
        return {"error": "Session not found"}

    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.desc())
        .limit(20)
        .all()
    )

    messages = list(reversed(messages))

    history = build_history(messages)

    user_message = Message(
        session_id=session_id,
        role="user",
        content=request.question
    )

    db.add(user_message)

    try:
        result = chatbot.ask(query=request.question, history=history)
    except TypeError:
        result = chatbot.ask(query=request.question)

    assistant_message = Message(
        session_id=session_id,
        role="assistant",
        content=result["answer"]
    )

    db.add(assistant_message)

    db.commit()

    return result
# <----- ----->