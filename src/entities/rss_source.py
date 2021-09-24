from typing import Optional

from pydantic import BaseModel


class RSSSource(BaseModel):
    name: Optional[str] = None
