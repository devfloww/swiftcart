from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import text # for debug

from core.db.database import get_db, engine
from core.db import models
from core.routes.users import router as users_router

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

# Routers
app.include_router(users_router)

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Swiftcart core API is running."}

### THESE ARE FOR QUICK TESTS
@app.get("/check_db")
async def check_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db_connection": result.scalar()}
