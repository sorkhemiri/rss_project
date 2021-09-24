import datetime
from typing import Optional

from pydantic import BaseModel

from .rss_source import RSSSource


class RSS(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    source: Optional[RSSSource] = None
    pub_date: Optional[datetime] = None
