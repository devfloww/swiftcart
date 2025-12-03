from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text # for debug
from core.db.database import get_db

# Globals and Configs
app = FastAPI(
    title="Swiftcart core API",
    debug=True,
    docs_url="/api/docs/"
)

@app.get("/")
async def root():
    return {"message": "Swiftcart core API is running."}


### THESE ARE FOR QUICK TESTS
@app.get("/check_db")
async def check_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db_connection": result.scalar()}

