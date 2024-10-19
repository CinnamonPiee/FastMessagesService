from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from src.database import get_db
from src.schemas import UserCreate, User
from src.models import User as UserModel


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(UserModel).filter(UserModel.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)
    new_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return RedirectResponse(url="/success", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(UserModel).filter(UserModel.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar()

    if not existing_user or not pwd_context.verify(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )

    return RedirectResponse(url="/success", status_code=status.HTTP_303_SEE_OTHER)
