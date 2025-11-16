from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.api.models.users import User
from src.core.config import config

ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def _truncate_to_bytes(password: str, max_bytes: int = 72) -> str:
    encoded = password.encode('utf-8')
    if len(encoded) <= max_bytes:
        return password
    truncated_bytes = encoded[:max_bytes]
    while truncated_bytes and truncated_bytes[-1] & 0xC0 == 0x80:
        truncated_bytes = truncated_bytes[:-1]
    return truncated_bytes.decode('utf-8', errors='ignore')

def hash_password(plain_pwd: str) -> str:
    truncated_str = _truncate_to_bytes(plain_pwd, 72)
    return pwd_context.hash(truncated_str)

def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    truncated_str = _truncate_to_bytes(plain_pwd, 72)
    return pwd_context.verify(truncated_str, hashed_pwd)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )   

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("=== AUTH DEBUG ===")
    print("Token received:", token)
    print("SECRET_KEY:", SECRET_KEY)
    print("ALGORITHM:", ALGORITHM)
    
    try:
        payload = decode_access_token(token)
        print("Decoded payload:", payload)
        user_id = payload.get("sub") if isinstance(payload, dict) else None
        print("User ID from token:", user_id)

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )
        user = db.query(User).filter(User.id == int(user_id)).first()
        print("User found:", user)
        print("==================")
        return user
    except Exception as e:
        print("Auth error:", str(e))
        print("==================")
        raise