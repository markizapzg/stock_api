from pydantic import BaseModel
from typing import Optional
from datetime import date

class Stock(BaseModel):
    company_name: str
    stock_symbol: str
    date: date
    close_price: float
