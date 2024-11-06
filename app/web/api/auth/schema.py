from pydantic import BaseModel


class AuthCreate(BaseModel):
    username: str
    password: str
