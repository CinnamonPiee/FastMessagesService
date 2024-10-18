from sqlalchemy.ext.asyncio import AsyncSession
from .models import User


async def create_user(db: AsyncSession, username: str, hashed_password: str, email: str):
    new_user = User(username=username,
                    hashed_password=hashed_password, email=email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
