from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.database import get_db
from src.schemas import UserCreate, User
from src.models import User as UserModel


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_user = UserModel(username=user.username,
                         email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=User)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email).first()
    if not existing_user or not pwd_context.verify(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    return existing_user
