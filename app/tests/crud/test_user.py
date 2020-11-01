from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreateAdmin, UserUpdateAdmin
from app.tests.utils.utils import random_lower_string


def test_create_user(db: Session) -> None:
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    user = crud.user.create(db, obj_in=user_in)
    assert user.username == username
    assert hasattr(user, "hashed_password")


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    user = crud.user.create(db, obj_in=user_in)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.username == user_2.username
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    username = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=True)
    user = crud.user.create(db, obj_in=user_in)

    new_password = random_lower_string()
    user_in_update = UserUpdateAdmin(password=new_password, is_admin=True)
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)

    assert user_2
    assert user.username == user_2.username
    assert verify_password(new_password, user_2.hashed_password)
