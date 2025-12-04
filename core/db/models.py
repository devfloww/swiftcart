from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Numeric,
    DateTime,
    Boolean,
    Enum as SQLEnum,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
import enum
from decimal import Decimal
from typing import Optional, List

class Base(DeclarativeBase):
    pass

class UserRole(enum.StrEnum):
    CUSTOMER = "customer"
    VENDOR = "vendor"
    ADMIN = "admin"
    
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime]= mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CUSTOMER)
    
    # relationships
    vendor: Mapped["Vendor"] = relationship("Vendor", back_populates="user", uselist=False)
    
class Vendor(Base):
    __tablename__ = "vendors"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)
    store_name: Mapped[str] = mapped_column(String(100), nullable=False)
    store_slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_number: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime]= mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    banner_url: Mapped[str] = mapped_column(String(500), nullable=True)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0.00"), server_default="0.00", nullable=False
    )
    
    # relationships
    user: Mapped["User"] = relationship("User", back_populates="vendor", uselist=False)
    products: Mapped["Product"] = relationship("Product", back_populates="vendor")

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vendor_id: Mapped[int] = mapped_column(Integer, ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, server_default=Decimal("0.0"))
    compare_at_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True, server_default=Decimal("0.0"))
    flash_sale_price = Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True, server_default=Decimal("0.0"))
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_flash_sale: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    images: Mapped[List[str]] = mapped_column(List[String], nullable=True)  # Store JSON as string
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    flash_ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime]= mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # relationships
    vendor: Mapped["Vendor"] = relationship("Vendor", back_populates="products")