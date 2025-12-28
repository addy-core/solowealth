# SoloWealth - Personal Finance Tracker
# models.py - SQLAlchemy ORM and Pydantic Models

from datetime import date, datetime
from typing import Optional, List
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel, Field

# Database Setup
DATABASE_URL = "sqlite:///./finance.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================
# SQLAlchemy ORM Models
# ============================================

class ConfigDB(Base):
    """Configuration table for app settings"""
    __tablename__ = "config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CategoryDB(Base):
    """Expense categories"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    icon = Column(String(50), default="📦")
    is_fixed = Column(Boolean, default=False)
    default_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    expenses = relationship("ExpenseDB", back_populates="category_rel")


class ExpenseDB(Base):
    """Expense records"""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, default=date.today)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    is_fixed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category_rel = relationship("CategoryDB", back_populates="expenses")


class InvestmentDB(Base):
    """Investment/Savings records"""
    __tablename__ = "investments"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, default=date.today)
    amount = Column(Float, nullable=False)
    type = Column(String(50), nullable=False)  # 'deposit', 'withdrawal', 'dividend'
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DebtDB(Base):
    """Debt/Loan tracking"""
    __tablename__ = "debts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    principal = Column(Float, nullable=False)
    remaining = Column(Float, nullable=False)
    interest_rate = Column(Float, default=0.0)
    monthly_payment = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MonthlySnapshotDB(Base):
    """Monthly financial snapshots for reports"""
    __tablename__ = "monthly_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    salary = Column(Float, nullable=False)
    total_expenses = Column(Float, nullable=False)
    total_savings = Column(Float, nullable=False)
    savings_rate = Column(Float, nullable=False)
    net_worth = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================
# Pydantic Schemas (Request/Response Models)
# ============================================

class StatusEnum(str, Enum):
    RICH = "Rich"
    NEUTRAL = "Neutral"
    POOR = "Poor"


# Config Schemas
class ConfigBase(BaseModel):
    key: str
    value: float
    description: Optional[str] = None


class ConfigCreate(ConfigBase):
    pass


class ConfigUpdate(BaseModel):
    value: float


class ConfigResponse(ConfigBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Category Schemas
class CategoryBase(BaseModel):
    name: str
    icon: str = "📦"
    is_fixed: bool = False
    default_amount: float = 0.0


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Expense Schemas
class ExpenseBase(BaseModel):
    date: date
    amount: float
    category_id: int
    is_fixed: bool = False
    notes: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    date: Optional[date] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None
    is_fixed: Optional[bool] = None
    notes: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# Investment Schemas
class InvestmentBase(BaseModel):
    date: date
    amount: float
    type: str
    description: Optional[str] = None


class InvestmentCreate(InvestmentBase):
    pass


class InvestmentResponse(InvestmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Debt Schemas
class DebtBase(BaseModel):
    name: str
    principal: float
    remaining: float
    interest_rate: float = 0.0
    monthly_payment: float = 0.0


class DebtCreate(DebtBase):
    pass


class DebtUpdate(BaseModel):
    remaining: Optional[float] = None
    monthly_payment: Optional[float] = None


class DebtResponse(DebtBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardStats(BaseModel):
    monthly_salary: float
    total_expenses: float
    remaining_balance: float
    savings_rate: float
    status: StatusEnum
    net_worth: float
    total_investments: float
    total_debts: float
    current_month: str
    fixed_expenses: float
    variable_expenses: float


class FixedExpenseSuggestion(BaseModel):
    category_id: int
    category_name: str
    suggested_amount: float
    already_logged: bool


class MonthlyReport(BaseModel):
    year: int
    month: int
    month_name: str
    salary: float
    total_expenses: float
    savings: float
    savings_rate: float
    status: StatusEnum
    expenses_by_category: dict


# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
