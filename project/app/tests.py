from django.test import TestCase

# Create your tests here.
# Directory structure
"""
myapi/
│
├── .env
├── requirements.txt
├── main.py
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   └── services/
│       ├── __init__.py
│       └── user.py
"""

# .env
"""
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
"""

# requirements.txt
"""
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
psycopg2-binary==2.9.9
pydantic==2.5.1
pydantic-settings==2.1.0
"""

# # app/config.py
# from pydantic_settings import BaseSettings
# from functools import lru_cache

# class Settings(BaseSettings):
#     DATABASE_URL: str
#     SECRET_KEY: str
#     ENVIRONMENT: str

#     class Config:
#         env_file = ".env"

# @lru_cache()
# def get_settings():
#     return Settings()

# # app/database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from .config import get_settings

# settings = get_settings()

# engine = create_engine(settings.DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # app/models/user.py
# from sqlalchemy import Column, Integer, String, DateTime
# from datetime import datetime
# from ..database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     username = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# # app/schemas/user.py
# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional

# class UserBase(BaseModel):
#     email: EmailStr
#     username: str

# class UserCreate(UserBase):
#     password: str

# class UserResponse(UserBase):
#     id: int
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True

# # app/services/user.py
# from sqlalchemy.orm import Session
# from ..models.user import User
# from ..schemas.user import UserCreate
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class UserService:
#     @staticmethod
#     def create_user(db: Session, user: UserCreate):
#         hashed_password = pwd_context.hash(user.password)
#         db_user = User(
#             email=user.email,
#             username=user.username,
#             hashed_password=hashed_password
#         )
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return db_user

#     @staticmethod
#     def get_user_by_email(db: Session, email: str):
#         return db.query(User).filter(User.email == email).first()

# # app/routes/user.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from ..database import get_db
# from ..schemas.user import UserCreate, UserResponse
# from ..services.user import UserService

# router = APIRouter()

# @router.post("/users/", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = UserService.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return UserService.create_user(db=db, user=user)

# @router.get("/users/{user_id}", response_model=UserResponse)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# # main.py
# from fastapi import FastAPI
# from app.routes import user
# from app.database import engine, Base

# # Create database tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Include routers
# app.include_router(user.router, prefix="/api/v1")