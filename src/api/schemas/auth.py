from pydantic import BaseModel
from src.api.models.users import User
import datetime as dt

class UserCreate(BaseModel):
    email: str 
    username: str 
    password: str 

class UserOut(BaseModel):
    id: int 
    username: str 
    email: str 
    created_at: dt.datetime
    updated_at: dt.datetime
    
class UserLogin(BaseModel):
    email: str
    password: str