from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import MessageCreate, Message
from src.models import Message as MessageModel


router = APIRouter()


@router.post("/messages/", response_model=Message)
async def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    new_message = MessageModel(sender_id=message.sender_id,
                               recipient_id=message.recipient_id, content=message.content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@router.get("/messages/{user_id}", response_model=list[Message])
async def get_messages(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(MessageModel).filter((MessageModel.sender_id == user_id) | (
        MessageModel.recipient_id == user_id)).all()
    return messages
