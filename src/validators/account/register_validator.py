from typing import Optional

from pydantic import BaseModel


class RegisterValidator(BaseModel):
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
