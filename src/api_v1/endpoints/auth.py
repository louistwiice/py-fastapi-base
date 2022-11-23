from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.crud import users as user_crud
from db.schemas import users as users_schemas
from core.dependencies import get_db, get_current_user


router = APIRouter(tags=['Authentication'])


@router.post("/register", response_model=users_schemas.User, description='Create a user', status_code=status.HTTP_201_CREATED)
def create_user(user: users_schemas.UserCreate, db: Session= Depends(get_db)):
    try:
        db_user = user_crud.create(db=db, user=user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': 'User already exists', 'error': str(e)})


@router.post("/login", response_model=users_schemas.TokenBase, description='Authenticate a user', status_code=status.HTTP_201_CREATED)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    response = user_crud.login(db, form_data)

    if response is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username/Email and password don't match"
        )

    return response


@router.get("/me", response_model=users_schemas.User, description='Get the current user')
def get_me(user: users_schemas.User = Depends(get_current_user), db: Session= Depends(get_db)):
    return user

