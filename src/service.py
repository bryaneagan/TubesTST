import pandas as pd 
import numpy as np
from prophet import Prophet
import os

# stockCode = input("kodeSaham : ")

# date = input("YYYY-MM-DD : ")

def stock_forecast(stockCode : str, date : str) :
    # def stock_forecast (stockCode, date) :
    outname = str(stockCode + ".JK.csv") 
    outdir = 'src/dataset'
    fullname = os.path.join(outdir, outname)

    data = pd.read_csv(fullname)
    print (data)

    #Only pick date and close price column
    data = data[["Date", "Close"]]

    data.columns = ["ds","y"]

    #fb prophet library
    prophet = Prophet(daily_seasonality=True)
    prophet.fit(data)

    future_dates = prophet.make_future_dataframe(periods=1825)
    predictions = prophet.predict(future_dates)

    #stock forecast
    predictions = predictions[["ds", "yhat"]]

    print (predictions)

    #search for price according to input date
    df = pd.DataFrame(predictions)
    select_indices = list(np.where(df["ds"] == date)[0])
    prediction_table = df.iloc[select_indices]
    df2 = pd.DataFrame(prediction_table)

    #return price 
    # print("IDR "+ str(df2.iloc[0,1]))
    return (float(df2.iloc[0,1]))

# print(stock_forecast(stockCode, date))
