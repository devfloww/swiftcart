from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_db
from core.db.schemas import UserCreate, UserRead
from core.db import models
from core.utils.security import hash_password

# Users Router
router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
    }
)

@router.post("/create", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(
        models.select(models.User).where(models.User.email == user_in.email.lower())
    )
    if existing_user.scalar() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    password_hash = hash_password(user_in.password)
    new_user = models.User(
        first_name=user_in.first_name.strip().title(),
        last_name=user_in.last_name.strip().title(),
        email=user_in.email.lower(),
        password_hash=password_hash,
        role=user_in.role
    )
    
    # DB trns
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.get("/me", response_model=UserRead)
async def read_users_me():
    return {"message": "This endpoint will return the current authenticated user's details."}