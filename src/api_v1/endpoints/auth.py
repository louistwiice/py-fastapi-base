from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.crud import users as user_crud
from db.schemas import users as users_schemas
from db.schemas import auth as auth_schemas
from core.dependencies import get_db, get_current_user
from utils.users.security import log_user, regenerate_token
from utils.users.services import verify_password


router = APIRouter(tags=['Authentication'])


@router.post("/register", response_model=users_schemas.User, description='Create a user', status_code=status.HTTP_201_CREATED)
def create_user(user: users_schemas.UserCreate, db: Session= Depends(get_db)):
    try:
        db_user = user_crud.create(db=db, user=user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': 'User already exists', 'error': str(e)})


@router.post("/login", response_model=auth_schemas.TokenBase, description='Authenticate a user', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    response = await log_user(db, form_data)

    if response is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username/Email and password don't match"
        )

    return response


@router.post("/refresh_token", response_model=auth_schemas.TokenBase, description='Refresh user token', status_code=status.HTTP_200_OK)
async def refresh_token(token: auth_schemas.RefreshTokenBase, db: Session= Depends(get_db)):
    response = regenerate_token(db, token.refresh_token)

    if response is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please, login again. Refresh token expired"
        )

    return response


@router.post("/change_password", description='Change a user password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(data: users_schemas.ChangePassword, user: users_schemas.User = Depends(get_current_user), db: Session= Depends(get_db)):

    if data.new_password != data.confirm_password:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='new_password and confirm_password do not match'
        )

    response = user_crud.update_password(db, str(user.id), data)

    if response is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )

    if isinstance(response, dict):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response
        )

    return {'message': 'Password reset successfully'}


@router.get("/me", response_model=users_schemas.User, description='Get the current user', status_code=status.HTTP_200_OK)
async def get_me(user: users_schemas.User = Depends(get_current_user)):
    return user

