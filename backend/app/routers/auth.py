from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.database import users_collection
from app.services.auth_service import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

# Define request models
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserRegister):
    """Endpoint to create a new user."""
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)
    new_user = {"username": user.username, "password": hashed_password}
    await users_collection.insert_one(new_user)
    return {"message": "User successfully created"}

@router.post("/login")
async def login(user: UserLogin):
    """Endpoint to authenticate a user and generate a JWT token."""
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username}, timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}
