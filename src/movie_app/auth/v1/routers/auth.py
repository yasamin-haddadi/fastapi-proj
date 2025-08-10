from fastapi import APIRouter, status, HTTPException, Depends
from movie_app.auth.v1.services.auth_service import AuthService
from movie_app.auth.v1.schemas import LoginRequest, TokenAccess
from movie_app.users.v1.schemas.user_schemas import UserResponseSchema
from fastapi import Response, Request
from movie_app.auth.v1.deps import get_auth_service
from movie_app.auth.v1.exceptions import (
    UserNotFoundError,
    InvalidCredentialsError,
    UserInactiveError,
    RoleNotAssignedError,
    InvalidTokenError,
)

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login', response_model=TokenAccess)
def login(data: LoginRequest, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    try:
        tokens = auth_service.login(data, response)
        return tokens
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserInactiveError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RoleNotAssignedError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/refresh', response_model=TokenAccess)
def refresh_token(request: Request, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    try:
        tokens = auth_service.refresh(request, response)
        return tokens
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserInactiveError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RoleNotAssignedError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/me', response_model=UserResponseSchema)
def get_current_user(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found in cookies")
    try:
        user = auth_service.get_current_user(token)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserInactiveError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RoleNotAssignedError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))



# Using DI here ensures consistent structure, easier testing,
# and flexibility for future changes even if logout is currently static.
@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response, auth_service: AuthService = Depends(get_auth_service)):
    auth_service.logout(response)