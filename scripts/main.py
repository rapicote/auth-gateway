# auth_gateway/main.py

from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from typing import List

from . import auth, models, schemas
from .config import settings
from .database import engine, SessionLocal
from .oauth2 import JWTBearer

app = FastAPI(
    title="API Gateway",
    description="Authentication API Gateway",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your_email@example.com",
        "url": "https://example.com",
    },
    license="MIT License",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me", response_model=schemas.User)
async def read_user_me(current_user: models.User = Depends(JWTBearer())):
    return current_user

@app.get("/users/", response_model=List[schemas.User])
async def read_users(db: SessionLocal = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/users/login")
async def login_for_access_token(form_data: schemas.UserLogin, db: SessionLocal = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = JWTBearer()
    return {"access_token": access_token}