from fastapi import FastAPI
from app.routes.stocks import router

# Kreiramo FastAPI aplikaciju
app = FastAPI(title="Stock API", version="1.0.0")

# Uključujemo rute
app.include_router(router, prefix="/api", tags=["Stocks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock API!"}