import bcrypt
import jwt
from dotenv import dotenv_values
from fastapi import APIRouter, Depends, HTTPException
from logic.db import get_db
from logic.models import User
from sqlalchemy.orm import Session
from starlette.requests import Request
import logging

config = dotenv_values("/.env")

JWT_SECRET = config["JWT_SECRET"]
JWT_ALGORITHM = config["JWT_ALGORITHM"]
JWT_SALT_LENGTH = int(config["JWT_SALT_LENGTH"])


router = APIRouter(prefix="/auth", tags=["Authentification"])


async def get_client_ip(request: Request) -> str:
    return request.client.host


def hash_password(password: str):
    return bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt(JWT_SALT_LENGTH)
    ).decode("utf-8")


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# TODO add captcha
@router.post(
    "/register",
)
async def register(
    email: str, password: str, full_name: str, db: Session = Depends(get_db)
):
    """Register new user with email/password"""
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    User.create_user(db, email, hashed_password, full_name=full_name)
    db.close()

    return {"message": "User registered successfully"}


@router.post(
    "/login",
)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login with email/password"""
    user = db.query(User).filter(User.email == email).first()
    db.close()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    jwt_token = jwt.encode({"sub": user.id}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {
        "access_token": jwt_token,
        "user": {"email": user.email, "full_name": user.full_name},
    }


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/info")
async def get_info(token: str, db : Session = Depends(get_db)):
    """Example of a protected route"""
    user_id = get_current_user(token)
    user = User.get_user_by_id(db, user_id)
    return {
        "user_id": user_id,
        "full_name": user.full_name,
        "email": user.email,
    }
