from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID
from movie_app.users.v1.schemas import user_schemas
from movie_app.users.v1.services.user_service import UserService
from movie_app.users.v1.deps import get_user_service
from movie_app.users.v1.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
)


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=user_schemas.PaginatedUsers)
def list_users(
                page: int = Query(1, ge=1, description='Page number, must be >= 1'),
                size: int = Query(10, ge=1, le=100, description='Page size, between 1 and 100'),
                user_service: UserService = Depends(get_user_service),
               ):
    users = user_service.get_all_users(page=page, size=size)
    return users

@router.get("/{user_id}", response_model=user_schemas.UserResponseSchema)
def get_user(user_id: UUID, user_service: UserService = Depends(get_user_service),):
    try:
        user = user_service.get_user_by_id(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=user_schemas.UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(user_in: user_schemas.UserCreateSchema, user_service: UserService = Depends(get_user_service),):
    try:
        user = user_service.create_user(user_in)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{user_id}", response_model=user_schemas.UserResponseSchema)
def update_user(user_id: UUID, user_in: user_schemas.UserUpdateSchema, user_service: UserService = Depends(get_user_service),):
    try:
        user = user_service.update_user(user_id, user_in)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service),):
    try:
        user_service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
