from pydantic import BaseModel
from typing import List, Any


class AuthResponse(BaseModel):
    user_token: str


class SessionCreate(BaseModel):
    title: str | None = None


class ChatRequest(BaseModel):
    message: str


class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int


class PaginatedResponse(BaseModel):
    data: List[Any]
    meta: PaginationMeta


class QAInput(BaseModel):
    question: str
    answer: str


class QAResponse(BaseModel):
    message: str
    status: str
    id: str | None = None