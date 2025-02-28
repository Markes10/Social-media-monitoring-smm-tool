from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from auth import pwd_context, create_access_token, authenticate_user
from database import get_db

router = APIRouter()

@router.post("/register")
def register(username: str, password: str, agency_id: int, role: str = "user", db: Session = Depends(get_db)):
    """Register a new user with an agency ID and role."""
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user = User(username=username, password=pwd_context.hash(password), role=role, agency_id=agency_id)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
