from typing import Optional

from pydantic import BaseModel


class RSSSource(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None

