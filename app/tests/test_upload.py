import pytest
import tempfile
from datetime import datetime

def test_upload_csv(test_client, test_db):
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as temp_csv:
        temp_csv.write("Date,Close\n2022-01-01,100\n2022-01-02,200\n")
        temp_csv_path = temp_csv.name

    with open(temp_csv_path, "rb") as file:
        response = test_client.post("/api/stocks/upload", files={"file": file})

    assert response.status_code == 200
    assert response.json()["message"] == "CSV file uploaded and data inserted successfully"

    # Verify data in the database
    stocks = list(test_db.stocks.find({"stock_symbol": "TEST"}))
    assert len(stocks) == 2
