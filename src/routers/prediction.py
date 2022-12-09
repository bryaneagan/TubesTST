from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from src.auth import AuthHandler
from src.schemas import StockDetails, stocks, DateInformation
from src.service import stock_forecast
import datetime
import requests

router = APIRouter(
    prefix = "/prediction",
    tags = ["prediction"]
)

auth_handler = AuthHandler()

@router.post('/stockforecast')
def stockforecast(stock_details : StockDetails,username=Depends(auth_handler.auth_wrapper)): 
    for stk in stocks :
        if f"{stock_details.stockCode}.JK" == stk:
            format_date = f"{stock_details.year}-{stock_details.month}-{stock_details.date}"
            if (datetime.datetime(stock_details.year,stock_details.month, stock_details.date) <= datetime.datetime(2027,12,6)) :
                stock_result = stock_forecast(stockCode = stock_details.stockCode, date = format_date)
                return {"stock price": stock_result}
            else :
                raise HTTPException(status_code=404, detail='Stock date is not available in forecast list')
    else : 
        raise HTTPException(status_code=404, detail='Stock code is not available in forecast list')


### Fetch forecast data from Modan's API
def fetch_data(type, amount):
    loginHeader = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    loginData = {
    "username": "xxxadminxxx",
    "password": "admin123"
    }
    loginResponse = requests.post("http://128.199.149.182:8069/user/login",headers=loginHeader,json=loginData)

    token = ""
    if loginResponse.status_code == 200:
        # Access the loginResponse data
        tokenData = loginResponse.json()
        token = tokenData["token"]
    else:
        print('Failed to fetch data')

    header = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    request_data = {
        "type": type,
        "amount": amount
    }
    recommended_stocks = []
    response = requests.post("http://128.199.149.182:8069/stock/recommended-stock",headers=header,json=request_data)
    if response.status_code == 200:
        # Access the response data
        data = response.json()
        recommended_stocks.append(data)
    else:
        print('Failed to fetch data')
    return recommended_stocks


@router.post("/stockrecommendation")
async def stockrecommendation(date : DateInformation,username=Depends(auth_handler.auth_wrapper)):
    return fetch_data(date.type, date.amount)