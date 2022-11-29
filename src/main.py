from DatabaseConnection import get_account_collection
from fastapi import FastAPI, Depends, HTTPException, Query
from .auth import AuthHandler
from .schemas import AuthDetails
import uuid

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
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    user_dict = {
        '_id': uuid.uuid4().hex,
        'username': auth_details.username,
        'password': hashed_password    
    }
    collection_of_users = get_account_collection()
    collection_of_users.insert_one(user_dict)
    return {"message" : "Successful Register"}

@app.post ('/login')
def login (auth_details: AuthDetails) : 
    user = None
    collection_of_users = get_account_collection()
    for user in collection_of_users.find({"username": auth_details.username}):
        if user["username"] == auth_details.username and auth_handler.verify_password(auth_details.password, user['password']):
            token = auth_handler.encode_token(user['username'])
            return { 'token': token }
    raise HTTPException(status_code=401, detail='Invalid username and/or password')

@app.get("/unprotected")
def unprotected():
    return {"hello": "world"}

@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)): 
    return {'name' : username}



