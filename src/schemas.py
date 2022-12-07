from pydantic import BaseModel
from fastapi import Query

class AuthDetails(BaseModel):
    username: str
    password: str

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password
        }
    
class StockDetails(BaseModel):
    stockCode : str 
    year: int
    month: int
    day : int




class StockInventory(BaseModel) :
    stockCode : str 
    stockAmount : int

#bluechip stocks by IDX per July 2022
stocks = ["ADRO.JK", "AMRT.JK", "ANTM.JK", "ASII.JK", "BBCA.JK", 
"BBNI.JK", "BBRI.JK", "BBTN.JK", "BFIN.JK", "BMRI.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK",
"EMTK.JK", "ERAA.JK", "EXCL.JK", "GGRM.JK", "HMSP.JK", "HRUM.JK", "ICBP.JK", "INCO.JK",
"INDF.JK", "INTP.JK", "ITMG.JK", "JPFA.JK", "KLBF.JK", "MDKA.JK", "MEDC.JK", "MIKA.JK",
"MNCN.JK", "PGAS.JK", "PTBA.JK", "PTPP.JK", "SMGR.JK", "TBIG.JK", "TIN S.JK", "TKIM.JK",
"TLKM.JK", "TOWR.JK", "TPIA.JK", "UNTR.JK", "UNVR.JK", "WIKA.JK", "WSKT.JK"]