# get_token_from_cookie_or_header

# from fastapi import Request
#
# def get_token_from_header(request: Request) -> str:
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer "):
#         raise ValueError("Invalid or missing Authorization header")
#     return auth_header.split(" ")[1]

#======================================================================



# from fastapi.security import OAuth2PasswordBearer
# from fastapi import Depends, HTTPException, status
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
#
# def get_token(token: str = Depends(oauth2_scheme)) -> str:
#         return token
#

#=======================================================================================================================================


from fastapi import Depends
from sqlalchemy.orm import Session
from movie_app.infrastructure.database.deps import get_db
from movie_app.auth.v1.services.auth_service import AuthService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)
