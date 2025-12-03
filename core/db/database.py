from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

# Globals and configs
load_dotenv(dotenv_path=".env")
DB_URL = os.getenv("DB_URL")
Base = declarative_base()
engine = create_async_engine(
    DB_URL,
    echo=True,
    future=True,
    connect_args={ "check_same_thread": False },
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

