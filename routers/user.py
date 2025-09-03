from fastapi import APIRouter, HTTPException
from uuid import UUID
from schemas.user import DeactivateUser, User, UserCreate, UserUpdate, Users, Response
from services.user import user_services

user_router = APIRouter()

# Get all users
@user_router.get("", response_model=Response, tags=["Users"])
def get_users():
    users = user_services.get_all_users()
    return Response(message="Users retrieved successfully", data=Users(users=users))

# Get user by ID
@user_router.get("/{id}", response_model=Response, tags=["Users"])
def get_user_by_id(id: UUID):
    user = user_services.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found")
    return Response(message="User retrieved successfully", data=user)

# Add a new user
@user_router.post("", response_model=Response, tags=["Users"])
def add_user(user_in: UserCreate):
    user = user_services.add_user(user_in)
    return Response(message="User added successfully", data=user)

# Update user
@user_router.put("/{id}", response_model=Response, tags=["Users"])
def update_user(id: UUID, user_in: UserUpdate):
    user = user_services.update_user(id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found")
    return Response(message="User updated successfully", data=user)

# Deactivate user
@user_router.patch("/{id}", response_model=Response, tags=["Users"])
def deactivate_user(id: UUID):
    user = user_services.deactivate_user(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found")
    return Response(message="User deactivated successfully", data=user)

# Delete user
@user_router.delete("/{id}", response_model=Response, tags=["Users"])
def delete_user(id: UUID):
    is_deleted = user_services.delete_user(id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found")
    return Response(message="User deleted successfully")