from fastapi import FastAPI

app = FastAPI(title="KFC Sales Forecast API")

@app.get("/")
async def root():
    return {"message": "Hello The Dragontail API is running."}