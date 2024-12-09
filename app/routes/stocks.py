from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta, date
from pymongo import ASCENDING
from bson import ObjectId
from app.database import db
from app.models import Stock
import csv
import os

router = APIRouter()

# Pomoćna funkcija za proveru vikenda i praznika
def is_weekend_or_holiday(dt):
    """Proverava da li je datum vikend ili praznik."""
    if dt.weekday() >= 5:  # Subota i nedelja
        return True
    holidays = [date(2022, 1, 1), date(2022, 12, 25)]  # Dodajte praznike
    if dt.date() in holidays:
        return True
    return False

# Pomoćna funkcija za višestruki profit
def calculate_total_profit(stocks):
    """Računa ukupan maksimalni profit kroz višestruke transakcije."""
    total_profit = 0
    for i in range(len(stocks) - 1):
        for j in range(i + 1, len(stocks)):
            if stocks[j]["close_price"] > stocks[i]["close_price"]:
                total_profit += stocks[j]["close_price"] - stocks[i]["close_price"]
                break
    return total_profit

# CRUD operacije
@router.get("/stocks")
def get_stocks(company_name: str = None, stock_symbol: str = None):
    query = {}
    if company_name:
        query["company_name"] = company_name
    if stock_symbol:
        query["stock_symbol"] = stock_symbol

    stocks = list(db.stocks.find(query))
    for stock in stocks:
        stock["_id"] = str(stock["_id"])  # Konvertujemo ObjectId u string
    return stocks

@router.post("/stocks")
def create_stock(stock: Stock):
    stock_data = stock.dict()
    stock_data["date"] = datetime.combine(stock_data["date"], datetime.min.time())
    result = db.stocks.insert_one(stock_data)
    return {"id": str(result.inserted_id)}

@router.put("/stocks/{id}")
def update_stock(id: str, stock: Stock):
    result = db.stocks.update_one({"_id": ObjectId(id)}, {"$set": stock.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"message": "Stock updated successfully"}

@router.delete("/stocks/{id}")
def delete_stock(id: str):
    result = db.stocks.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"message": "Stock deleted successfully"}

# Proračun profita
@router.get("/stocks/{stock_symbol}/profit")
def calculate_profit(stock_symbol: str, start_date: str, end_date: str):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")

    stocks = list(db.stocks.find({
        "stock_symbol": stock_symbol,
        "date": {"$gte": start_date, "$lte": end_date}
    }).sort("date", ASCENDING))

    stocks = [stock for stock in stocks if not is_weekend_or_holiday(stock["date"])]

    if not stocks:
        raise HTTPException(status_code=404, detail="No data for the given date range")

    min_price = min(stocks, key=lambda x: x["close_price"])
    max_price = max(stocks, key=lambda x: x["close_price"])
    profit = max_price["close_price"] - min_price["close_price"]

    return {
        "symbol": stock_symbol,
        "date_range": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        },
        "buy_date": min_price["date"],
        "buy_price": min_price["close_price"],
        "sell_date": max_price["date"],
        "sell_price": max_price["close_price"],
        "profit": profit,
        "total_profit": calculate_total_profit(stocks)
    }

# Prošireni proračun profita
@router.get("/stocks/{stock_symbol}/profit_extended")
def calculate_profit_extended(stock_symbol: str, start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    period_days = (end_date - start_date).days + 1

    prev_start_date = start_date - timedelta(days=period_days)
    prev_end_date = start_date - timedelta(days=1)
    next_start_date = end_date + timedelta(days=1)
    next_end_date = end_date + timedelta(days=period_days)

    periods = {
        "current": {"start": start_date, "end": end_date},
        "previous": {"start": prev_start_date, "end": prev_end_date},
        "next": {"start": next_start_date, "end": next_end_date},
    }

    results = {}
    for period_name, dates in periods.items():
        stocks = list(db.stocks.find({
            "stock_symbol": stock_symbol,
            "date": {"$gte": dates["start"], "$lte": dates["end"]}
        }).sort("date", ASCENDING))

        stocks = [stock for stock in stocks if not is_weekend_or_holiday(stock["date"])]

        if not stocks:
            results[period_name] = {"error": "No data found"}
            continue

        min_price = min(stocks, key=lambda x: x["close_price"])
        max_price = max(stocks, key=lambda x: x["close_price"])
        profit = max_price["close_price"] - min_price["close_price"]

        results[period_name] = {
            "buy_date": min_price["date"],
            "buy_price": min_price["close_price"],
            "sell_date": max_price["date"],
            "sell_price": max_price["close_price"],
            "profit": profit,
            "total_profit": calculate_total_profit(stocks)
        }

    return results

# Učitavanje CSV fajlova
@router.post("/stocks/upload")
def upload_csv(file_path: str = Query(...)):
    try:
        base_name = os.path.basename(file_path)
        company_name, _ = os.path.splitext(base_name)
        stock_symbol = company_name[:4].upper()

        with open(file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            batch = []

            for row in reader:
                if not all(key in row for key in ["Date", "Close"]):
                    continue
                if row["Close"] in (None, '', 'null'):
                    continue

                try:
                    date = datetime.strptime(row["Date"], "%Y-%m-%d")
                    if is_weekend_or_holiday(date):
                        continue
                except ValueError:
                    continue

                try:
                    close_price = float(row["Close"])
                except ValueError:
                    continue

                stock = {
                    "company_name": company_name,
                    "stock_symbol": stock_symbol,
                    "date": date,
                    "close_price": close_price,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                batch.append(stock)

            if batch:
                db.stocks.insert_many(batch, ordered=False)

        return {"message": f"File '{file_path}' uploaded and data inserted successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File '{file_path}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
