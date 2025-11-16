from src.api.models.users import User
from src.api.schemas.auth import UserCreate, UserLogin, UserOut
from fastapi import APIRouter, HTTPException, Depends
from src.core.auth import hash_password, verify_password, create_access_token, get_current_user
from src.core.database import get_db
from sqlalchemy.orm import Session 

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=UserOut)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user_data.email,
        User.username == user_data.username
    ).first()
    if db_user:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists!"
        )
    hashed_password = hash_password(user_data.password)
    try:
        new_user = User(
            username = user_data.username,
            email = user_data.email,
            hashed_password = hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        print(f"Exception: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not add user!"
        )
    
@router.post("/login")
async def user_login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == login_data.email
    ).first()
    if db_user is None or not verify_password(login_data.password, str(db_user.hashed_password)):
        raise HTTPException(    
            status_code=401,
            detail="Invalid Username or Password"
        )
    access_token = create_access_token({"sub": str(db_user.id)})
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "message": "Login Successful",
        "user": {
            "username": db_user.username,
            "email": db_user.email 
        } 
    }
    
@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user