# from fastapi import Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from movie_app.auth.v1.services.auth_service import AuthService
# from movie_app.users.v1.models.user import UserModel
# from movie_app.infrastructure.database.deps import get_db
#
#
# def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
#     return AuthService(db)
#
# from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
#
#
# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     auth_service: AuthService = Depends(get_auth_service)) -> UserModel:
#     return auth_service.get_current_user(token)
#
#
#
# def has_permission(permission_name: str):
#     def dependency(
#             current_user: UserModel = Depends(get_current_user),
#             db: Session = Depends(get_db)
#     ):
#         # اگر کاربر نقش نداشت (مثلاً حذف شده یا غیر فعال)
#         if not current_user.role:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="User has no assigned role."
#             )
#
#         # بارگذاری permission ها از DB برای نقش کاربر (اگر lazy بارگذاری نشد)
#         role = db.query(type(current_user.role)).filter_by(id=current_user.role.id).first()
#         if not role:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Role not found."
#             )
#
#         # چک کردن اینکه permission مورد نظر در نقش کاربر هست یا نه
#         permissions = {perm.name for perm in role.permissions}
#         if permission_name not in permissions:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Permission '{permission_name}' required."
#             )
#
#         return True
#
#     return dependency
