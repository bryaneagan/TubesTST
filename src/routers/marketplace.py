from fastapi import APIRouter
from src.DatabaseConnection import get_stock_collection, get_history_collection
from fastapi import FastAPI, Depends, HTTPException
from src.auth import AuthHandler
from src.schemas import stocks, StockInventory
import uuid
from datetime import datetime

router = APIRouter(
    prefix = "/marketplace",
    tags = ["marketplace"]
)
auth_handler = AuthHandler()

@router.post('/buystock')
def buystock(stock_inventory : StockInventory,username=Depends(auth_handler.auth_wrapper)):
    stock_dict = {
        '_id' : stock_inventory.stockCode,
        'stockAmount' : stock_inventory.stockAmount
    }
    transaction_dict = {
        '_id': uuid.uuid4().hex,
        'timestamp' : str(datetime.date(datetime.now())),
        'transaction' : 'buy',
        'stockCode' : stock_inventory.stockCode,
        'stockAmount' : stock_inventory.stockAmount
    }
    collection_of_stocks = get_stock_collection()
    collection_of_history = get_history_collection()
    input_history = collection_of_history.insert_one(transaction_dict)
    for stk in stocks :
        if f"{stock_inventory.stockCode}.JK" == stk:
            store = collection_of_stocks.find_one({"_id" : stock_inventory.stockCode})
            if store : 
                collection_of_stocks.update_one({"_id" : stock_inventory.stockCode}, {
                        "$inc" : {"stockAmount" : stock_inventory.stockAmount}
                })  
            else:
                collection_of_stocks.insert_one(stock_dict)
                print(transaction_dict)
            input_history
            return {"message": "Purchase was successful!"}
    raise HTTPException(status_code=404, detail='Stock is unavailable')

@router.post('/sellstock')
def sellstock(stock_invetory : StockInventory,username=Depends(auth_handler.auth_wrapper)): 
    stock_dict = {
        '_id' : stock_invetory.stockCode,
        'stockAmount' : stock_invetory.stockAmount
    }
    transaction_dict = {
        '_id': uuid.uuid4().hex,
        'timestamp' : str(datetime.date(datetime.now())),
        'transaction' : 'sell',
        'stockCode' : stock_invetory.stockCode,
        'stockAmount' : stock_invetory.stockAmount
    }
    collection_of_stocks = get_stock_collection()
    collection_of_history = get_history_collection()
    input_history = collection_of_history.insert_one(transaction_dict)
    temp = collection_of_stocks.find_one({"_id" : stock_invetory.stockCode})
    if temp:
        print(temp)
        if  int(temp["stockAmount"]) >= stock_invetory.stockAmount : 
            collection_of_stocks.update_one({"_id" : stock_invetory.stockCode}, {
                "$inc" : {"stockAmount" : -stock_invetory.stockAmount}
            })
            if int(temp["stockAmount"]) - stock_invetory.stockAmount <= 0:
                collection_of_stocks.delete_one({"_id" : stock_invetory.stockCode})
            input_history
            return {"message" : "Sales was successful!"}
        else :
            raise HTTPException(status_code=402, detail='The amount of stock owned is insufficient')
    else :
            raise HTTPException(status_code=404, detail='Stock is not found in inventory')

@router.get("/stockinventory")
def stockinventory(username=Depends(auth_handler.auth_wrapper)) :
    stock_list = []
    collection_of_stocks = get_stock_collection()
    result =  collection_of_stocks.find({})
    for stock in result:
        print(stock)
        stock_list.append(stock)
    return {"stock inventory" : stock_list}

@router.get("/transactionhistory")
def transactionhistory(username=Depends(auth_handler.auth_wrapper)) :
    transaction_history = []
    collection_of_history = get_history_collection()
    result =  collection_of_history.find({})
    print (collection_of_history)
    for history in result:
        print(history)
        transaction_history.append(history)
    return {"transaction history" : transaction_history}