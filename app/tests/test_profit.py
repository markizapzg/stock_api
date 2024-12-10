import pytest
from datetime import datetime

def test_calculate_profit(test_client, test_db):
    # Insert mock data into the test database
    test_db.stocks.insert_many([
        {
            "company_name": "Test Company",
            "stock_symbol": "TEST",
            "date": datetime(2022, 1, 1),
            "close_price": 100.0
        },
        {
            "company_name": "Test Company",
            "stock_symbol": "TEST",
            "date": datetime(2022, 1, 2),
            "close_price": 200.0
        }
    ])

    # Log the inserted data
    print("Inserted Data:", list(test_db.stocks.find()))

    # Test profit calculation
    response = test_client.get("/api/stocks/TEST/profit?start_date=2022-01-01&end_date=2022-01-02")
    assert response.status_code == 200
    assert response.json()["profit"] == 100.0
