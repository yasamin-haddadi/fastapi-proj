from sqlalchemy.orm import Session
from movie_app.users.v1.crud.user_crud import UserCRUD
from movie_app.users.v1.schemas import user_schemas
from movie_app.users.v1.models.user import UserModel
from typing import Optional
from movie_app.core.security import hash_password
from uuid import UUID
from movie_app.core.logging_config import get_logger
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from movie_app.users.v1.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    UserInactiveError,
)


logger = get_logger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_crud = UserCRUD(db)

    def get_all_users(self, page: int = 1, size: int = 10) -> user_schemas.PaginatedUsers:
        total, users = self.user_crud.get_all_users(page=page, size=size)
        return user_schemas.PaginatedUsers(
            total=total,
            page=page,
            size=size,
            users=users
        )

    def get_user_by_id(self, user_id: UUID) -> Optional[UserModel]:
        """Retrieve user by UUID. Returns None if not found."""
        user = self.user_crud.get_user_by_id(user_id)
        if not user:
            logger.info(f"User with id {user_id} not found.")
            raise UserNotFoundError(f"User with id {user_id} not found.")
        return user

    def create_user(self, user_in: user_schemas.UserCreateSchema) -> UserModel:
        """Create user with hashed password."""
        hashed_pwd = hash_password(user_in.password)
        try:
            user = self.user_crud.create_user(user_in=user_in, hashed_password=hashed_pwd)
            logger.info(f"User created with email: {user.email}")
            return user
        except IntegrityError as e:
            logger.error(f"Integrity error while creating user: {e}")
            raise UserAlreadyExistsError("User with this email or username already exists.")
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating user: {e}")
            raise


    def update_user(self, user_id: UUID, user_in: user_schemas.UserUpdateSchema) -> Optional[UserModel]:
        update_data = user_in.model_dump(exclude_unset=True)

        if 'password' in update_data:
            update_data['hashed_password'] = hash_password(update_data.pop('password'))

        user = self.user_crud.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User with id {user_id} not found for update.")
            raise UserNotFoundError(f"User with id {user_id} not found.")

        try:
            updated_user = self.user_crud.update_user(user_id=user_id, update_in=update_data)
            logger.info(f"User with id {user_id} updated.")
            return updated_user
        except SQLAlchemyError as e:
            logger.error(f"Database error on user update: {e}")
            raise


    def delete_user(self, user_id: UUID) -> None:
        user = self.user_crud.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User with id {user_id} not found for deletion.")
            raise UserNotFoundError(f"User with id {user_id} not found.")

        try:
            self.user_crud.delete_user(user_id)
            logger.info(f"User with id {user_id} deleted.")
        except SQLAlchemyError as e:
            logger.error(f"Database error on user deletion: {e}")
            raise
