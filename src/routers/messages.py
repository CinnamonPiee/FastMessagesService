from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas import MessageCreate, Message
from src.models import Message as MessageModel


router = APIRouter()


@router.post("/messages/", response_model=Message)
async def send_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    new_message = MessageModel(sender_id=message.sender_id,
                               receiver_id=message.receiver_id, content=message.content)
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    return new_message


@router.get("/messages/{user_id}", response_model=list[Message])
async def get_messages(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(MessageModel).filter(
        or_(
            MessageModel.sender_id == user_id,
            MessageModel.receiver_id == user_id
        )
    )
    result = await db.execute(stmt)
    messages = result.scalars().all()
    if not messages:
        raise HTTPException(status_code=404, detail="Messages not found")

    return messages
