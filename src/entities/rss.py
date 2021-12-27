from datetime import date
from typing import Optional

from pydantic import BaseModel

from .rss_source import RSSSource


class RSS(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    source: Optional[RSSSource] = None
    pub_date: Optional[date] = None

    def dict(self, *args, **kwargs):
        data = super(RSS, self).dict(*args, **kwargs)
        if data.get("pub_date"):
            data["pub_date"] = data["pub_date"].strftime("%Y-%m-%d")
        return data
