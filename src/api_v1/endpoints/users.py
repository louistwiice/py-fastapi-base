from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from db.crud import users as user_crud
from db.schemas import users as users_schemas
from core.dependencies import get_db


router = APIRouter(tags=['Users'])


@router.post("/{user_id}/picture", response_model=users_schemas.User, description='Upload or Edit user profile picture', status_code=status.HTTP_200_OK)
async def upload_picture(user_id: str, picture: UploadFile, db: Session= Depends(get_db)):
    try:
        if not picture.filename.endswith('.jpeg'):
            raise Exception('Allowed files are extension .jpeg only')

        db_user = user_crud.upload_picture(db, user_id, picture)
        if db_user:
            return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message':  str(e)})

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': 'User not found'})


@router.get("/", response_model=list[users_schemas.User], description='List all users')
def list_users(skip: int = 0, limit: int = 100, db: Session= Depends(get_db)):
    users = user_crud.list_all(db, skip, limit)
    return users


@router.get("/{user_id}", response_model=users_schemas.User, description='Retrieve a user by ID')
def read_user_by_id(user_id: str, db: Session= Depends(get_db)):
    try:
        db_user = user_crud.get_by_id(db, user_id)
        if db_user:
            return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail={'message': 'User not found', 'error': str(e)})

    raise HTTPException(status_code=400, detail={'message': 'User not found'})


@router.patch("/{user_id}", response_model=users_schemas.User, description='Update user information')
def update_user(user_id: str, user_data: users_schemas.UserUpdate, db: Session= Depends(get_db)):
    try:
        db_user = user_crud.update(db, user_id, user_data)
        if db_user:
            return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail={'message': 'User not found', 'error': str(e)})

    raise HTTPException(status_code=400, detail={'message': 'User not found'})
