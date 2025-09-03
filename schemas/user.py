
from pydantic import BaseModel

from typing import Optional


class User(BaseModel):
     id : str
     name: str 
     email: str
     is_active : bool 


class UserCreate(BaseModel):
     name: str 
     email: str
     is_active : bool 

class UserUpdate(BaseModel):   
     name: Optional[str] = None
     email: Optional[str] = None
     

class DeactivateUser(BaseModel):

    is_active : bool = False
    

class Users(BaseModel):
    users: list[User]


class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[User | Users] = None
