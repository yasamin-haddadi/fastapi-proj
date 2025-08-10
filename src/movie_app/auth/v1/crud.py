from sqlalchemy.orm import Session
from movie_app.users.v1.models.user import UserModel
from typing import Optional


class AuthCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return user

    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return user

