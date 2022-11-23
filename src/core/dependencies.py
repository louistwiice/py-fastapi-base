from datetime import datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError

from db.models.users import User
from db.database import SessionLocal
from core.config import settings


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=settings.API_V1_NAME+"/auth/login",
    scheme_name="JWT"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        print("===== ", token)

        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == username).first()
    if user is None:
        raise credentials_exception
    return user
