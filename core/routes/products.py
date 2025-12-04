from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_db
from core.db.schemas import ProductCreate, ProductRead
from core.db import models

router = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={
        404: { "description": "Not Found"}
    }
)
