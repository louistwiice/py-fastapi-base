import os
import shutil

import pytz
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.config import ROOT_DIRECTORY
from db.models import users as models
from db.schemas import users as users_schemas
from utils.common import generate_string
from utils.users.services import hashed_password, verify_password


def create(db: Session, user: users_schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=False,
        is_superuser=False,
        is_staff=user.is_staff,
        password=hashed_password(user.password),
        updated_at=datetime.now(tz=pytz.UTC)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


def get_by_id(db: Session, user_id: str) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def get_by_username(db: Session, username: str) -> models.User:
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


def update(db: Session, user_id: str, user_data: users_schemas.UserUpdate) -> models.User:
    db_user = get_by_id(db, user_id)
    if not db_user:
        return None

    db_user.username = user_data.username if user_data.username is not None else db_user.username
    db_user.first_name = user_data.first_name if user_data.first_name is not None else db_user.first_name
    db_user.last_name = user_data.last_name if user_data.last_name is not None else db_user.last_name
    db_user.email = user_data.email if user_data.email is not None else db_user.email
    db_user.is_staff = user_data.is_staff if user_data.is_staff is not None else db_user.is_staff
    db_user.updated_at = datetime.now(tz=pytz.UTC)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_password(db: Session, user_id: str, data: users_schemas.ChangePassword):
    db_user = get_by_id(db, user_id)

    if not verify_password(data.old_password, db_user.password):
        return {'error': 'This is not your actual password'}

    hashed_pass = hashed_password(data.new_password)
    db_user.password = hashed_pass
    db_user.updated_at = datetime.now(tz=pytz.UTC)
    db.commit()
    db.refresh(db_user)
    return db_user


def upload_picture(db: Session, user_id: str, picture: UploadFile):
    db_user = get_by_id(db, user_id)
    if not db_user:
        return None

    users_file_location = "media/users"

    if not os.path.isdir(users_file_location):
        os.mkdir(users_file_location)

    filename = f'{picture.filename[:-5]}_{generate_string(20)}.jpeg'
    file_location = f"{ROOT_DIRECTORY}/{users_file_location}/{filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(picture.file, file_object)

    db_user.picture = f'{users_file_location}/{filename}'
    db.commit()
    db.refresh(db_user)
    return db_user

