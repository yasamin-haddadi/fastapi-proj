from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from movie_app.infrastructure.database.base import Base
from movie_app.users.v1.models.role_permission import role_permission


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    permissions = relationship(
        "Permission",
        secondary=role_permission,
        back_populates="roles"
    )

    users = relationship(
        "UserModel",
        back_populates="role",
        passive_deletes=True
    )
