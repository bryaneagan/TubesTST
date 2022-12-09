from fastapi import FastAPI
from .schemas import stocks
from .routers import marketplace, prediction, user

app = FastAPI()

app.include_router(user.router)
app.include_router(prediction.router)
app.include_router(marketplace.router)

users = []

@app.get("/")
async def root():
    print(users)
    return {"message": "Welcome to Bryan Eagan - 18220041 's Stock Marketplace and Stock Forecast Simulation API"}


@app.get("/stocklist")
def stocklist() :
    return {"stock list" : stocks}
    


