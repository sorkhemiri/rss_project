from pydantic import BaseModel


class LoginValidator(BaseModel):
    username: str
    password: str
