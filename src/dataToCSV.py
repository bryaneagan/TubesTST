import datetime as dt
from itertools import count
import pandas_datareader as web
import os


start = dt.datetime(2020,1,1)
end = dt.datetime.now()

#bluechip stocks by IDX per July 2022
stocks = ["ADRO.JK", "AMRT.JK", "ANTM.JK", "ASII.JK", "BBCA.JK", 
"BBNI.JK", "BBRI.JK", "BBTN.JK", "BFIN.JK", "BMRI.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK",
"EMTK.JK", "ERAA.JK", "EXCL.JK", "GGRM.JK", "HMSP.JK", "HRUM.JK", "ICBP.JK", "INCO.JK",
"INDF.JK", "INTP.JK", "ITMG.JK", "JPFA.JK", "KLBF.JK", "MDKA.JK", "MEDC.JK", "MIKA.JK",
"MNCN.JK", "PGAS.JK", "PTBA.JK", "PTPP.JK", "SMGR.JK", "TBIG.JK", "TIN S.JK", "TKIM.JK",
"TLKM.JK", "TOWR.JK", "TPIA.JK", "UNTR.JK", "UNVR.JK", "WIKA.JK", "WSKT.JK"]

for i in range (len(stocks)) : 
    data = web.DataReader (stocks[i], "yahoo")
    outname = str(stocks[i] + ".csv") 
    outdir = 'D:\BES FILES\Institut Teknologi Bandung\Year 3\Semester 5\Teknologi Sistem Terintegrasi\Tubes\MongoDB\TubesTST\dataset'
    fullname = os.path.join(outdir, outname)
    data.to_csv(fullname)

