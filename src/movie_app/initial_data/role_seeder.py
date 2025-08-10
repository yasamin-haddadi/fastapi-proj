from sqlalchemy.orm import Session
from movie_app.users.v1.models.role import Role
from sqlalchemy import or_

def seed_roles(db: Session):
    roles = [
        {"id": 1, "name": "admin", "description": "Administrator role"},
        {"id": 2, "name": "user", "description": "Default user role"},
        {"id": 3, "name": "moderator", "description": "Moderator role"},
    ]

    for role_data in roles:
        role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if role:
            continue
        else:
            new_role = Role(**role_data)
            db.add(new_role)

    db.commit()


