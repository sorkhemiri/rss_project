from typing import List

from entities import User
from interfaces.validator import ValidatorInterface


class RSSDataStruct(ValidatorInterface):
    source_key: str
    rss_ids: List[int]


class RemoveFromUnseenValidator(ValidatorInterface):
    rss_data: List[RSSDataStruct]
    user: User
