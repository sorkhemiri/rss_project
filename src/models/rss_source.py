from tortoise import fields

from .base import BaseModel


class RSSSource(BaseModel):
    title = fields.CharField(max_length=300, required=True)
    link = fields.CharField(max_length=500, required=True)
    key = fields.CharField(max_length=100, required=True)
    description = fields.CharField(max_length=800)
    need_update = fields.BooleanField(default=False)

    def __str__(self):
        return self.title
