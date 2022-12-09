from fastapi import APIRouter
from src.DatabaseConnection import get_account_collection
from fastapi import FastAPI, Depends, HTTPException
from src.auth import AuthHandler
from src.schemas import AuthDetails

router = APIRouter(
    prefix = "/user",
    tags = ["user"]
)

auth_handler = AuthHandler()

@router.post('/register') 
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
    return {"message" : "Register Success!"}

@router.post ('/login')
def login (auth_details: AuthDetails) : 
    user = None
    collection_of_users = get_account_collection()
    for user in collection_of_users.find({"username": auth_details.username}):
        if user["username"] == auth_details.username and auth_handler.verify_password(auth_details.password, user['password']):
            token = auth_handler.encode_token(user['username'])
            return { 'token': token }
    raise HTTPException(status_code=401, detail='Username and/or password is invalid')