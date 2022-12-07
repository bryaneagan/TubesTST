import datetime as dt
from itertools import count
import pandas_datareader as web
import os
from .schemas import stocks

start = dt.datetime(2020,1,1)
end = dt.datetime.now()



for i in range (len(stocks)) : 
    data = web.DataReader (stocks[i], "yahoo")
    outname = str(stocks[i] + ".csv") 
    outdir = 'D:\BES FILES\Institut Teknologi Bandung\Year 3\Semester 5\Teknologi Sistem Terintegrasi\Tubes\MongoDB\TubesTST\dataset'
    fullname = os.path.join(outdir, outname)
    data.to_csv(fullname)

