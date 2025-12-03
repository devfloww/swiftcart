from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import text # for debug

from core.db.database import get_db, engine
from core.db.schemas import UserCreate, UserRead
from core.db import models
from core.utils.security import hash_password

# Fastapi lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    print("\nDatabase connected and tables created (if not exist).\n")
    yield
    # shutdown
    await engine.dispose()
    print("\nDatabase connection closed.\n")
    

# Globals and Configs
app = FastAPI(
    title="Swiftcart core API",
    lifespan=lifespan,
    debug=True,
    docs_url="/api/docs/",
)


@app.get("/api")
async def root():
    return {"message": "Swiftcart core API is running."}


### THESE ARE FOR QUICK TESTS
@app.get("/check_db")
async def check_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db_connection": result.scalar()}

@app.post("/api/users/create", response_model=UserRead, status_code=status.HTTP_201_CREATED)
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