from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    uid: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

    def dict(self, *args, **kwargs):
        data = super(User, self).dict(*args, **kwargs)
        if data.get("uid"):
            data["uid"] = str(data["uid"])
        return data
