from tortoise import fields

from .base import BaseModel


class Like(BaseModel):
    rss = fields.ForeignKeyField(
        "models.RSS", related_name="likes", null=True, on_delete=fields.CASCADE
    )
    user = fields.ForeignKeyField(
        "models.User", related_name="likes", null=True, on_delete=fields.CASCADE
    )
