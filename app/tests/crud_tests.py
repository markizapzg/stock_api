import pytest


def test_create_stock(test_client, test_db):
    # Test creating a stock
    response = test_client.post("/api/stocks", json={
        "company_name": "Test Company",
        "stock_symbol": "TEST",
        "date": "2022-01-01",
        "close_price": 100.0
    })
    assert response.status_code == 200
    stock_id = response.json()["id"]

    # Verify the stock exists in the database
    stock = test_db.stocks.find_one({"_id": stock_id})
    assert stock is not None


def test_update_stock(test_client, test_db):
    # Insert a stock to update
    stock_id = test_db.stocks.insert_one({
        "company_name": "Test Company",
        "stock_symbol": "TEST",
        "date": "2022-01-01",
        "close_price": 100.0
    }).inserted_id

    # Update the stock
    response = test_client.put(f"/api/stocks/{stock_id}", json={
        "company_name": "Updated Company",
        "stock_symbol": "TEST",
        "date": "2022-01-01",
        "close_price": 200.0
    })
    assert response.status_code == 200

    # Verify the update in the database
    stock = test_db.stocks.find_one({"_id": stock_id})
    assert stock["company_name"] == "Updated Company"
    assert stock["close_price"] == 200.0


def test_delete_stock(test_client, test_db):
    # Insert a stock to delete
    stock_id = test_db.stocks.insert_one({
        "company_name": "Test Company",
        "stock_symbol": "TEST",
        "date": "2022-01-01",
        "close_price": 100.0
    }).inserted_id

    # Delete the stock
    response = test_client.delete(f"/api/stocks/{stock_id}")
    assert response.status_code == 200

    # Verify the stock is deleted
    stock = test_db.stocks.find_one({"_id": stock_id})
    assert stock is None
