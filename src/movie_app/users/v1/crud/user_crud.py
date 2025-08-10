from typing import Optional, Tuple
from movie_app.users.v1.models.user import UserModel
from sqlalchemy.orm import Session
from movie_app.users.v1.schemas import user_schemas
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self, page: int = 1, size: int = 10) -> Tuple[int, list[UserModel]]:
        skip = (page - 1) * size
        total = self.db.query(UserModel).count()
        users = self.db.query(UserModel).offset(skip).limit(size).all()
        return total, users


    def get_user_by_id(self, user_id: UUID) -> Optional[UserModel]:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return user

    def create_user(self, user_in: user_schemas.UserCreateSchema, hashed_password: str) -> UserModel:
        user = UserModel(
            email=user_in.email,
            username=user_in.username,
            full_name=user_in.full_name,
            hashed_password=hashed_password,
            role_id=user_in.role_id,
            is_active=user_in.is_active,
        )
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            raise


    def update_user(self, user_id: UUID, update_in: dict) -> Optional[UserModel]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        for field, value in update_in.items():
            setattr(user, field, value)

        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise


    def delete_user(self, user_id: UUID) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        try:
            self.db.delete(user)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise
