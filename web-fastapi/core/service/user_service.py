from typing import Optional

from sqlalchemy.orm import Session

from core.po.user import User
from core.vo.base import UserCreateVo


def get_users_page(db: Session, offset: int, limit: int) -> list[User]:
    return db.query(User).offset(offset).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, vo: UserCreateVo) -> User:
    user = User(name=vo.name, age=vo.age, email=vo.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True
