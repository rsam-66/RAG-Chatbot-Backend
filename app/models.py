from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_token = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sessions = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), default="New Chat")

    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    session_id = Column(Integer, ForeignKey("sessions.id"))

    role = Column(String(20))
    content = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="messages")


# Data Models
class PaketWisata(Base):
    __tablename__ = "paket_wisata"

    id = Column(Integer, primary_key=True)
    data_id = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HargaTiket(Base):
    __tablename__ = "harga_tiket"

    id = Column(Integer, primary_key=True)
    group_name = Column(String(255))
    item_name = Column(String(255))
    price = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True)
    data_id = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TempatPenting(Base):
    __tablename__ = "tempat_penting"

    id = Column(Integer, primary_key=True)
    data_id = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class NomorPenting(Base):
    __tablename__ = "nomor_penting"

    id = Column(Integer, primary_key=True)
    data_id = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    phone = Column(String(20))
    address = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Wisata(Base):
    __tablename__ = "wisata"

    id = Column(Integer, primary_key=True)
    data_id = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Transportasi(Base):
    __tablename__ = "transportasi"

    id = Column(Integer, primary_key=True)
    section_name = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())