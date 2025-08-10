from movie_app.auth.v1.crud import AuthCRUD
from movie_app.users.v1.crud.user_crud import UserCRUD
from movie_app.users.v1.models.user import UserModel
from movie_app.auth.v1.schemas import LoginRequest, TokenAccess
from movie_app.core import security
from sqlalchemy.orm import Session
from fastapi import Response, Request
from movie_app.auth.v1.exceptions import (
    UserNotFoundError,
    InvalidCredentialsError,
    UserInactiveError,
    RoleNotAssignedError,
    InvalidTokenError,
)

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.auth_crud = AuthCRUD(db)
        self.user_crud = UserCRUD(db)

    @staticmethod
    def _set_tokens_in_cookies( response: Response, access_token: str, refresh_token: str) -> None:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="strict",
            max_age=60 * 15
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="strict",
            max_age=60 * 60 * 24 * 7  # ۷ روز
        )

    def login(self, data: LoginRequest, response: Response) -> TokenAccess:
        user = self.auth_crud.get_user_by_email(str(data.email))
        if not user:
            raise InvalidCredentialsError("Invalid credentials")
        if not security.verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError("Invalid credentials")

        if not user.is_active:
            raise UserInactiveError("User is inactive")

        if not user.role:
            raise RoleNotAssignedError("User has no role assigned")

        token_data = {
            "sub": str(user.id),
            "role": user.role.name,
        }


        access_token = security.create_access_token(data=token_data)
        refresh_token = security.create_refresh_token(data=token_data)

        self._set_tokens_in_cookies(response, access_token, refresh_token)

        return TokenAccess(
            access_token=access_token,
            refresh_token=refresh_token,
            #token_type="bearer",
        )

    def refresh(self, request: Request, response: Response) -> TokenAccess:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise InvalidTokenError("Refresh token not found")

        try:
            payload = security.decode_refresh_token(refresh_token)
            user_id = payload.get("sub")
            if user_id is None:
                raise InvalidTokenError("Invalid token payload")

            user = self.user_crud.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundError("User not found")

            if not user.is_active:
                raise UserInactiveError("User is inactive")

            if not user.role:
                raise RoleNotAssignedError("User has no role assigned")

            token_data = {
                "sub": str(user.id),
                "role": user.role.name
            }
            new_access_token = security.create_access_token(data=token_data)
            new_refresh_token = security.create_refresh_token(data=token_data)

            self._set_tokens_in_cookies(response, new_access_token, new_refresh_token)

            return TokenAccess(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                #token_type= "bearer",
            )

        except Exception:
            raise InvalidTokenError("Invalid refresh token")


    def get_current_user(self, token: str) -> UserModel:
        payload = security.decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError("Invalid token payload")

        user = self.user_crud.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        if not user.is_active:
            raise UserInactiveError("User is inactive")

        if not user.role:
            raise RoleNotAssignedError("User has no role assigned")

        return user

    @staticmethod
    def logout(response: Response) -> None:
            response.delete_cookie(key="access_token")
            response.delete_cookie(key="refresh_token")
