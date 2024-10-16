from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)

    messages_sent = relationship(
        "Message", foreign_keys="[Message.sender_id]", back_populates="sender")
    messages_received = relationship(
        "Message", foreign_keys="[Message.receiver_id]", back_populates="receiver")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))

    sender = relationship("User", foreign_keys=[
                          sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[
                            receiver_id], back_populates="messages_received")
