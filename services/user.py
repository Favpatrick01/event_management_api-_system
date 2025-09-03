from uuid import uuid4, UUID
from fastapi import HTTPException
from database import user_db
from schemas.user import User, UserCreate, UserUpdate
from typing import List, Optional


class UserServices:

    @staticmethod
    def get_all_users() -> List[User]:
        return list(user_db.values())

    @staticmethod
    def get_user_by_id(id: UUID) -> Optional[User]:
        return user_db.get(str(id))

    @staticmethod
    def add_user(user_in: UserCreate) -> User:
        """
        Create a new user after validating that the name is unique (case-insensitive).
        """
        UserServices._validate_unique_name(user_in.name)

        user = User(
            id=str(uuid4()),
            **user_in.model_dump()
        )

        user_db[user.id] = user
        return user

    @staticmethod
    def _validate_unique_name(name: str) -> None:
        """
        Check if a user with the same name already exists.
        Raises HTTPException if a duplicate is found.
        """
        if any(u.name.lower() == name.lower() for u in user_db.values()):
            raise HTTPException(
                status_code=400,
                detail=f"User with name '{name}' already exists."
            )

    @staticmethod
    def update_user(id: UUID, user_in: UserUpdate) -> Optional[User]:
        user = user_db.get(str(id))
        if not user:
            return None

        if user_in.name is not None:
            user.name = user_in.name
        if user_in.email is not None:
            user.email = user_in.email

        return user

    @staticmethod
    def deactivate_user(id: UUID) -> Optional[User]:
        user = user_db.get(str(id))
        if not user:
            return None

        user.is_active = False
        user_db[str(id)] = user
        return user

    @staticmethod
    def delete_user(id: UUID) -> bool:
        user_id = str(id)
        if user_id not in user_db:
            return False

        del user_db[user_id]
        return True


user_services = UserServices()