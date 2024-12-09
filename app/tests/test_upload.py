import pytest
from pathlib import Path


def test_upload_csv(test_client, test_db):
    # Prepare a temporary CSV file for testing
    temp_csv = Path("/tmp/test.csv")
    temp_csv.write_text("Date,Close\n2022-01-01,100\n2022-01-02,200\n")

    # Call the upload endpoint
    response = test_client.post(f"/api/stocks/upload?file_path={temp_csv}")
    assert response.status_code == 200
    assert "uploaded and data inserted successfully" in response.json()["message"]

    # Verify data in the database
    stocks = list(test_db.stocks.find({"stock_symbol": "TEST"}))
    assert len(stocks) == 2

    # Clean up temporary file
    temp_csv.unlink()
