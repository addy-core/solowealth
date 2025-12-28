# SoloWealth - Personal Finance Tracker
# main.py - FastAPI Backend

import sys
import io

# Fix for Uvicorn logging in windowed mode (PyInstaller --noconsole)
# When running without a console, sys.stdout and sys.stderr are None
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

import csv
import os
from datetime import date, datetime
from typing import List, Optional
from calendar import month_name

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import extract

from models import (
    ConfigDB, CategoryDB, ExpenseDB, InvestmentDB, DebtDB,
    ConfigUpdate, ConfigResponse, CategoryCreate, CategoryResponse,
    ExpenseCreate, ExpenseUpdate, ExpenseResponse,
    InvestmentCreate, InvestmentResponse,
    DebtCreate, DebtUpdate, DebtResponse,
    DashboardStats, FixedExpenseSuggestion, MonthlyReport, StatusEnum,
    init_db, get_db, engine
)

app = FastAPI(
    title="SoloWealth",
    description="Local-only Personal Finance Tracker",
    version="1.0.0"
)

def seed_database():
    db = Session(engine)
    try:
        if db.query(ConfigDB).first() is not None:
            db.close()
            return
        configs = [
            ConfigDB(key="monthly_salary", value=100000.0, description="Monthly salary"),
            ConfigDB(key="base_investments", value=200000.0, description="Initial investments"),
        ]
        db.add_all(configs)
        categories = [
            CategoryDB(name="Rent", icon="home", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Utilities", icon="zap", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Gym", icon="dumbbell", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Groceries", icon="shopping-cart", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Family", icon="users", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Loan", icon="landmark", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Food", icon="utensils", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Transport", icon="car", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Entertainment", icon="film", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Shopping", icon="shopping-bag", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Healthcare", icon="heart-pulse", is_fixed=False, default_amount=0.0),
            CategoryDB(name="Other", icon="package", is_fixed=False, default_amount=0.0),
        ]
        db.add_all(categories)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()
    seed_database()

# Config Endpoints
@app.get("/api/config", response_model=List[ConfigResponse])
def get_all_config(db: Session = Depends(get_db)):
    return db.query(ConfigDB).all()

@app.get("/api/config/{key}", response_model=ConfigResponse)
def get_config(key: str, db: Session = Depends(get_db)):
    config = db.query(ConfigDB).filter(ConfigDB.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail=f"Config '{key}' not found")
    return config

@app.put("/api/config/{key}", response_model=ConfigResponse)
def update_config(key: str, config_update: ConfigUpdate, db: Session = Depends(get_db)):
    config = db.query(ConfigDB).filter(ConfigDB.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail=f"Config '{key}' not found")
    config.value = config_update.value
    config.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(config)
    return config

# Category Endpoints
@app.get("/api/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryDB).all()

@app.post("/api/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(CategoryDB).filter(CategoryDB.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    db_category = CategoryDB(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/api/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if db.query(ExpenseDB).filter(ExpenseDB.category_id == category_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete category with expenses")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}

# Expense Endpoints
@app.get("/api/expenses", response_model=List[ExpenseResponse])
def get_expenses(month: Optional[int] = None, year: Optional[int] = None, 
                 category_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(ExpenseDB)
    if month:
        query = query.filter(extract('month', ExpenseDB.date) == month)
    if year:
        query = query.filter(extract('year', ExpenseDB.date) == year)
    if category_id:
        query = query.filter(ExpenseDB.category_id == category_id)
    expenses = query.order_by(ExpenseDB.date.desc()).all()
    result = []
    for exp in expenses:
        result.append(ExpenseResponse(
            id=exp.id, date=exp.date, amount=exp.amount, category_id=exp.category_id,
            is_fixed=exp.is_fixed, notes=exp.notes, created_at=exp.created_at,
            updated_at=exp.updated_at, category_name=exp.category_rel.name if exp.category_rel else None
        ))
    return result

@app.post("/api/expenses", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    category = db.query(CategoryDB).filter(CategoryDB.id == expense.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_expense = ExpenseDB(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return ExpenseResponse(
        id=db_expense.id, date=db_expense.date, amount=db_expense.amount,
        category_id=db_expense.category_id, is_fixed=db_expense.is_fixed,
        notes=db_expense.notes, created_at=db_expense.created_at,
        updated_at=db_expense.updated_at, category_name=category.name
    )

@app.put("/api/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in expense.dict(exclude_unset=True).items():
        setattr(db_expense, key, value)
    db_expense.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_expense)
    return ExpenseResponse(
        id=db_expense.id, date=db_expense.date, amount=db_expense.amount,
        category_id=db_expense.category_id, is_fixed=db_expense.is_fixed,
        notes=db_expense.notes, created_at=db_expense.created_at,
        updated_at=db_expense.updated_at, 
        category_name=db_expense.category_rel.name if db_expense.category_rel else None
    )

@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}

# Investment Endpoints
@app.get("/api/investments", response_model=List[InvestmentResponse])
def get_investments(year: Optional[int] = None, type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(InvestmentDB)
    if year:
        query = query.filter(extract('year', InvestmentDB.date) == year)
    if type:
        query = query.filter(InvestmentDB.type == type)
    return query.order_by(InvestmentDB.date.desc()).all()

@app.post("/api/investments", response_model=InvestmentResponse)
def create_investment(investment: InvestmentCreate, db: Session = Depends(get_db)):
    db_investment = InvestmentDB(**investment.dict())
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    return db_investment

@app.put("/api/investments/{investment_id}", response_model=InvestmentResponse)
def update_investment(investment_id: int, investment: InvestmentCreate, db: Session = Depends(get_db)):
    db_investment = db.query(InvestmentDB).filter(InvestmentDB.id == investment_id).first()
    if not db_investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    for key, value in investment.dict(exclude_unset=True).items():
        setattr(db_investment, key, value)
    db_investment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_investment)
    return db_investment

@app.delete("/api/investments/{investment_id}")
def delete_investment(investment_id: int, db: Session = Depends(get_db)):
    investment = db.query(InvestmentDB).filter(InvestmentDB.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    db.delete(investment)
    db.commit()
    return {"message": "Investment deleted"}

# Debt Endpoints
@app.get("/api/debts", response_model=List[DebtResponse])
def get_debts(db: Session = Depends(get_db)):
    return db.query(DebtDB).all()

@app.post("/api/debts", response_model=DebtResponse)
def create_debt(debt: DebtCreate, db: Session = Depends(get_db)):
    db_debt = DebtDB(**debt.dict())
    db.add(db_debt)
    db.commit()
    db.refresh(db_debt)
    return db_debt

@app.put("/api/debts/{debt_id}", response_model=DebtResponse)
def update_debt(debt_id: int, debt: DebtUpdate, db: Session = Depends(get_db)):
    db_debt = db.query(DebtDB).filter(DebtDB.id == debt_id).first()
    if not db_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    for key, value in debt.dict(exclude_unset=True).items():
        setattr(db_debt, key, value)
    db_debt.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_debt)
    return db_debt

@app.delete("/api/debts/{debt_id}")
def delete_debt(debt_id: int, db: Session = Depends(get_db)):
    debt = db.query(DebtDB).filter(DebtDB.id == debt_id).first()
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    db.delete(debt)
    db.commit()
    return {"message": "Debt deleted"}

# Dashboard
@app.get("/api/dashboard", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    today = date.today()
    salary_config = db.query(ConfigDB).filter(ConfigDB.key == "monthly_salary").first()
    base_inv_config = db.query(ConfigDB).filter(ConfigDB.key == "base_investments").first()
    monthly_salary = salary_config.value if salary_config else 100000.0
    base_investments = base_inv_config.value if base_inv_config else 200000.0
    
    month_expenses = db.query(ExpenseDB).filter(
        extract('month', ExpenseDB.date) == today.month,
        extract('year', ExpenseDB.date) == today.year
    ).all()
    
    total_expenses = sum(e.amount for e in month_expenses)
    fixed_expenses = sum(e.amount for e in month_expenses if e.is_fixed)
    remaining_balance = monthly_salary - total_expenses
    savings_rate = (remaining_balance / monthly_salary) * 100 if monthly_salary > 0 else 0
    
    status = StatusEnum.RICH if savings_rate > 40 else (StatusEnum.NEUTRAL if savings_rate >= 15 else StatusEnum.POOR)
    
    investments = db.query(InvestmentDB).all()
    deposits = sum(i.amount for i in investments if i.type == 'deposit')
    withdrawals = sum(i.amount for i in investments if i.type == 'withdrawal')
    dividends = sum(i.amount for i in investments if i.type == 'dividend')
    total_investments = base_investments + deposits - withdrawals + dividends
    
    debts = db.query(DebtDB).all()
    total_debts = sum(d.remaining for d in debts)
    
    return DashboardStats(
        monthly_salary=monthly_salary, total_expenses=total_expenses,
        remaining_balance=remaining_balance, savings_rate=round(savings_rate, 2),
        status=status, net_worth=total_investments - total_debts,
        total_investments=total_investments, total_debts=total_debts,
        current_month=f"{month_name[today.month]} {today.year}",
        fixed_expenses=fixed_expenses, variable_expenses=total_expenses - fixed_expenses
    )

@app.get("/api/fixed-expense-suggestions", response_model=List[FixedExpenseSuggestion])
def get_fixed_expense_suggestions(db: Session = Depends(get_db)):
    today = date.today()
    fixed_cats = db.query(CategoryDB).filter(CategoryDB.is_fixed == True, CategoryDB.default_amount > 0).all()
    suggestions = []
    for cat in fixed_cats:
        existing = db.query(ExpenseDB).filter(
            ExpenseDB.category_id == cat.id, ExpenseDB.is_fixed == True,
            extract('month', ExpenseDB.date) == today.month,
            extract('year', ExpenseDB.date) == today.year
        ).first()
        suggestions.append(FixedExpenseSuggestion(
            category_id=cat.id, category_name=cat.name,
            suggested_amount=cat.default_amount, already_logged=existing is not None
        ))
    return suggestions

@app.post("/api/apply-fixed-expenses")
def apply_fixed_expenses(db: Session = Depends(get_db)):
    today = date.today()
    fixed_cats = db.query(CategoryDB).filter(CategoryDB.is_fixed == True, CategoryDB.default_amount > 0).all()
    applied, skipped = [], []
    for cat in fixed_cats:
        existing = db.query(ExpenseDB).filter(
            ExpenseDB.category_id == cat.id, ExpenseDB.is_fixed == True,
            extract('month', ExpenseDB.date) == today.month,
            extract('year', ExpenseDB.date) == today.year
        ).first()
        if existing:
            skipped.append(cat.name)
            continue
        expense = ExpenseDB(
            date=date(today.year, today.month, 1), amount=cat.default_amount,
            category_id=cat.id, is_fixed=True, notes=f"Auto-applied for {month_name[today.month]}"
        )
        db.add(expense)
        applied.append(cat.name)
    db.commit()
    return {"message": f"Applied {len(applied)} fixed expenses", "applied": applied, "skipped": skipped}

@app.get("/api/reports/monthly", response_model=List[MonthlyReport])
def get_monthly_reports(year: Optional[int] = None, db: Session = Depends(get_db)):
    query_year = year or date.today().year
    salary_config = db.query(ConfigDB).filter(ConfigDB.key == "monthly_salary").first()
    monthly_salary = salary_config.value if salary_config else 100000.0
    reports = []
    for month in range(1, 13):
        expenses = db.query(ExpenseDB).filter(
            extract('month', ExpenseDB.date) == month,
            extract('year', ExpenseDB.date) == query_year
        ).all()
        if not expenses:
            continue
        total = sum(e.amount for e in expenses)
        savings = monthly_salary - total
        savings_rate = (savings / monthly_salary) * 100 if monthly_salary > 0 else 0
        status = StatusEnum.RICH if savings_rate > 40 else (StatusEnum.NEUTRAL if savings_rate >= 15 else StatusEnum.POOR)
        expenses_by_cat = {}
        for exp in expenses:
            cat_name = exp.category_rel.name if exp.category_rel else "Unknown"
            expenses_by_cat[cat_name] = expenses_by_cat.get(cat_name, 0) + exp.amount
        reports.append(MonthlyReport(
            year=query_year, month=month, month_name=month_name[month],
            salary=monthly_salary, total_expenses=total, savings=savings,
            savings_rate=round(savings_rate, 2), status=status, expenses_by_category=expenses_by_cat
        ))
    return reports

@app.get("/api/export")
def export_data(db: Session = Depends(get_db)):
    export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_export.csv")
    expenses = db.query(ExpenseDB).all()
    with open(export_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Date', 'Amount', 'Category', 'Is Fixed', 'Notes', 'Created At'])
        for exp in expenses:
            writer.writerow([exp.id, exp.date.isoformat(), exp.amount,
                exp.category_rel.name if exp.category_rel else "Unknown",
                exp.is_fixed, exp.notes or "", exp.created_at.isoformat()])
    return FileResponse(path=export_path, filename="finance_export.csv", media_type="text/csv")

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
