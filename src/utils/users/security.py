from datetime import datetime

from fastapi import  HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from core.auth import create_access_token, create_refresh_token
from core.config import settings
from db.models import users as models
from utils.users.services import verify_password


async def log_user(db: Session, form_data: OAuth2PasswordRequestForm):
    get_username = db.query(models.User).filter(models.User.username == form_data.username).first()

    user = get_username if get_username is not None else db.query(models.User).filter(models.User.email == form_data.username).first()
    if user is None:
        return None

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        return None

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "Bearer",
    }


def regenerate_token(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate Refresh Token Information",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh Token expired. Please login",
                headers={"WWW-Authenticate": "Bearer"},
            )
        username: str = payload.get("sub")

    except JWTError:
        raise credentials_exception

    return {
        "access_token": create_access_token(username),
        "refresh_token": create_refresh_token(username),
        "token_type": "Bearer",
    }

