from DatabaseConnection import get_account_collection, get_stock_collection
from fastapi import FastAPI, Depends, HTTPException, Query
from .auth import AuthHandler
from .schemas import AuthDetails, StockDetails, stocks, StockInventory
import uuid
from .service import stock_forecast


app = FastAPI()

auth_handler = AuthHandler()
users = []

@app.get("/")
async def root():
    print(users)
    return {"message": "Tubes TST milik Bryan Eagan NIM 18220041"}

@app.post('/register') 
def register (auth_details: AuthDetails) : 
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username sudah tersedia')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    user_dict = {
        '_id': uuid.uuid4().hex,
        'username': auth_details.username,
        'password': hashed_password    
    }
    collection_of_users = get_account_collection()
    collection_of_users.insert_one(user_dict)
    return {"message" : "Register Sukses"}

@app.post ('/login')
def login (auth_details: AuthDetails) : 
    user = None
    collection_of_users = get_account_collection()
    for user in collection_of_users.find({"username": auth_details.username}):
        if user["username"] == auth_details.username and auth_handler.verify_password(auth_details.password, user['password']):
            token = auth_handler.encode_token(user['username'])
            return { 'token': token }
    raise HTTPException(status_code=401, detail='Username dan/atau password tidak tepat')

@app.get("/stocklist")
def stocklist() :
    return stocks
    
@app.post('/stockforecast')
def stockforecast(stock_details : StockDetails): 
    for stk in stocks :
        if f"{stock_details.stockCode}.JK" == stk:
            format_date = f"{stock_details.year}-{stock_details.month}-{stock_details.day}"
            stock_result = stock_forecast(stockCode = stock_details.stockCode, date = format_date)
            return {"value": stock_result}
    else : 
        return {"message" : "Saham tidak tersedia dalam list forecast"}


@app.post('/buystock')
def buystock(stock_inventory : StockInventory):
    stock_dict = {
        '_id' : stock_inventory.stockCode,
        'stockAmount' : stock_inventory.stockAmount
    }
    collection_of_stocks = get_stock_collection()
    for stk in stocks :
        if f"{stock_inventory.stockCode}.JK" == stk:
            store = collection_of_stocks.find_one({"_id" : stock_inventory.stockCode})
            if store :
                collection_of_stocks.update_one({"_id" : stock_inventory.stockCode}, {
                        "$inc" : {"stockAmount" : stock_inventory.stockAmount}
                })
            else:
                collection_of_stocks.insert_one(stock_dict)
            return {"message": "Pembelian sukses"}
    return {"message" : "Saham tidak tersedia"}

@app.post('/sellstock')
def sellstock(stock_invetory : StockInventory): 
    stock_dict = {
        '_id' : stock_invetory.stockCode,
        'stockAmount' : stock_invetory.stockAmount
    }
    collection_of_stocks = get_stock_collection()
    temp = collection_of_stocks.find_one({"_id" : stock_invetory.stockCode})
    if temp:
        print(temp)
        if  int(temp["stockAmount"]) >= stock_invetory.stockAmount : 
            collection_of_stocks.update_one({"_id" : stock_invetory.stockCode}, {
                "$inc" : {"stockAmount" : -stock_invetory.stockAmount}
            })
            if int(temp["stockAmount"]) - stock_invetory.stockAmount <= 0:
                collection_of_stocks.delete_one({"_id" : stock_invetory.stockCode})
            return {"message" : "Penjualan sukses"}
        else :
            return {"message" : "Jumlah saham yang dimiliki tidak cukup"}
    else :
            return {"message" : "Saham tidak ditemukan"}


@app.get("/stockinventory")
def stockinventory() :
    stock_list = []
    collection_of_stocks = get_stock_collection()
    result =  collection_of_stocks.find({})
    print(result)
    for stock in result:
        print(stock)
        stock_list.append(stock)
    return {"stock list" : stock_list}




