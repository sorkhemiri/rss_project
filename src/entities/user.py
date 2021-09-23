from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None
