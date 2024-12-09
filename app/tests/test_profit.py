import pytest


def test_calculate_profit(test_client, test_db):
    # Insert mock data into the test database
    test_db.stocks.insert_many([
        {
            "company_name": "Test Company",
            "stock_symbol": "TEST",
            "date": "2022-01-01T00:00:00",
            "close_price": 100.0
        },
        {
            "company_name": "Test Company",
            "stock_symbol": "TEST",
            "date": "2022-01-02T00:00:00",
            "close_price": 200.0
        }
    ])

    # Test profit calculation
    response = test_client.get("/api/stocks/TEST/profit?start_date=2022-01-01&end_date=2022-01-02")
    assert response.status_code == 200
    assert response.json()["profit"] == 100.0


def test_calculate_extended_profit(test_client, test_db):
    test_db.stocks.insert_many([
        {
            "company_name": "Test Company",
            "stock_symbol": "TEST",
            "date": "2022-01-01T00:00:00",
            "close_price": 100.0
        },
        {
            "company_name": "Test Company",
            "stock_symbol": "TEST",
            "date": "2022-01-02T00:00:00",
            "close_price": 200.0
        }
    ])

    response = test_client.get("/api/stocks/TEST/profit_extended?start_date=2022-01-01&end_date=2022-01-10")
    assert response.status_code == 200
    assert "current" in response.json()
    assert "previous" in response.json()
    assert "next" in response.json()


def test_total_profit(test_client, test_db):
    test_db.stocks.insert_many([
        {
            "company_name": "Test Company",
            "stock_symbol": "TEST",
            "date": "2022-01-01T00:00:00",
            "close_price": 100.0
        },
        {
            "company_name": "Test Company",
            "stock_symbol": "TEST",
            "date": "2022-01-02T00:00:00",
            "close_price": 200.0
        }
    ])

    response = test_client.get("/api/stocks/TEST/profit?start_date=2022-01-01&end_date=2022-01-10")
    assert response.status_code == 200
    assert "total_profit" in response.json()
    assert response.json()["total_profit"] > 0
