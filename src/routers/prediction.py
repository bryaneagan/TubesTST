from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from src.auth import AuthHandler
from src.schemas import StockDetails, stocks
from src.service import stock_forecast

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
            stock_result = stock_forecast(stockCode = stock_details.stockCode, date = format_date)
            return {"value": stock_result}
    else : 
        raise HTTPException(status_code=404, detail='Stock is not available in forecast list')