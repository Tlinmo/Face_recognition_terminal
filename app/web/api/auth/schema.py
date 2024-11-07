from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

class UpdateUser(BaseModel):
    id: Optional[UUID]
    username: str
    embeddings: Optional[List[float]]

    class Config:
        from_attributes = True 

class User(BaseModel):
    id: Optional[UUID]
    username: str
    is_superuser: bool
    embeddings: Optional[List[float]]

    class Config:
        from_attributes = True 