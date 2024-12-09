# Stock API

A FastAPI-based application for managing and analyzing stock market data.

## Features

- Upload CSV files to populate stock data into MongoDB.
- Perform CRUD operations on stock data.
- Calculate profit for a given stock symbol over a date range.
- Calculate extended profit across multiple periods.
- Easily deployable using Docker.

---

## Installation and Setup

### Prerequisites

- **Docker**: Ensure Docker and Docker Compose are installed on your machine.
- **Python 3.8**: Required for local development if not using Docker.

---

### Clone the Repository

```bash
git clone https://github.com/markizapzg/stock_api.git
cd stock_api

Running the Application with Docker

    Build and Start the Containers:

docker-compose up --build -d

Access the API:

    Open your browser or use a tool like curl or Postman to access:

        http://127.0.0.1:8000

    MongoDB Instance:
        MongoDB is exposed on port 27018.

API Endpoints
1. Upload a CSV File

    Endpoint: /api/stocks/upload
    Method: POST
    Query Parameter: file_path - Absolute path to the CSV file.
    Example:

    curl -X POST "http://127.0.0.1:8000/api/stocks/upload?file_path=/app/uploads/Facebook.csv"

2. Get All Stocks

    Endpoint: /api/stocks
    Method: GET
    Example:

    curl -X GET "http://127.0.0.1:8000/api/stocks"

3. Get Stocks by Company or Symbol

    Endpoint: /api/stocks
    Method: GET
    Query Parameters:
        company_name (optional)
        stock_symbol (optional)
    Example:

    curl -X GET "http://127.0.0.1:8000/api/stocks?company_name=Facebook&stock_symbol=FACE"

4. Add a Stock Record

    Endpoint: /api/stocks
    Method: POST
    Request Body:

{
    "company_name": "Facebook",
    "stock_symbol": "FACE",
    "date": "2020-06-01",
    "close_price": 250.0
}

Example:

    curl -X POST "http://127.0.0.1:8000/api/stocks" \
         -H "Content-Type: application/json" \
         -d '{"company_name": "Facebook", "stock_symbol": "FACE", "date": "2020-06-01", "close_price": 250.0}'

5. Delete a Stock Record

    Endpoint: /api/stocks/{id}
    Method: DELETE
    Example:

    curl -X DELETE "http://127.0.0.1:8000/api/stocks/67575a341684008092fe4f31"

6. Calculate Profit

    Endpoint: /api/stocks/{stock_symbol}/profit
    Method: GET
    Query Parameters:
        start_date (required)
        end_date (required)
    Example:

    curl -X GET "http://127.0.0.1:8000/api/stocks/FACE/profit?start_date=2020-06-01&end_date=2020-06-30"

7. Calculate Extended Profit

    Endpoint: /api/stocks/{stock_symbol}/profit_extended
    Method: GET
    Query Parameters:
        start_date (required)
        end_date (required)
    Example:

    curl -X GET "http://127.0.0.1:8000/api/stocks/FACE/profit_extended?start_date=2020-06-01&end_date=2020-06-30"

Running Tests

    Install pytest (if running locally):

pip install pytest

Run the Tests:

pytest
