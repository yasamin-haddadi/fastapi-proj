# from fastapi import Depends, HTTPException, status
# from movie_app.users.roles import UserRole
# from movie_app.auth.v1.deps import get_current_user
#
# def require_role(required_roles: list[UserRole]):
#     def dependency(current_user=Depends(get_current_user)):
#         if current_user.role not in required_roles:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Permission denied"
#             )
#         return current_user
#     return dependency
