import pymongo 

link = "mongodb+srv://bryaneagan:semangatdansukses@cluster0.ajuuphp.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(link)
db = client.account

def get_account_collection() :
    return db["userdata"]

def get_stock_collection() :
    return db["stockdata"]