from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from movie_app.infrastructure.database.base import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    roles = relationship("Role", secondary="role_permission", back_populates="permissions")


