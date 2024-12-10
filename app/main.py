from fastapi import FastAPI, HTTPException, UploadFile, File
from pymongo import MongoClient
import csv
from io import StringIO
from datetime import datetime

app = FastAPI(title="Stock API", version="1.0.0")

client = MongoClient("mongodb://mongo:27017/")
db = client["test_db"]

@app.post("/api/stocks/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV file and insert its data into the MongoDB collection.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are allowed.")

    content = await file.read()
    csv_data = csv.DictReader(StringIO(content.decode("utf-8")))
    records = []
    for row in csv_data:
        try:
            record = {
                "date": datetime.strptime(row["Date"], "%Y-%m-%d"),
                "close_price": float(row["Close"]),
                "stock_symbol": "TEST"  # You can update this based on your logic
            }
            records.append(record)
        except (ValueError, KeyError) as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {e}")

    db.stocks.insert_many(records)
    return {"message": "CSV file uploaded and data inserted successfully"}

@app.get("/api/stocks/{symbol}/profit")
def calculate_profit(symbol: str, start_date: str, end_date: str):
    """
    Endpoint to calculate profit for a stock within a date range.
    """
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    data = list(db.stocks.find({"stock_symbol": symbol, "date": {"$gte": start_date, "$lte": end_date}}))
    if not data:
        raise HTTPException(status_code=404, detail="No data for the given date range")

    profit = data[-1]["close_price"] - data[0]["close_price"]
    return {"profit": profit}
