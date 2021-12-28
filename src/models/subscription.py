from tortoise import fields

from .base import BaseModel


class Subscription(BaseModel):
    source = fields.ForeignKeyField(
        "models.RSSSource",
        related_name="subscriptions",
        null=True,
        on_delete=fields.CASCADE,
    )
    user = fields.ForeignKeyField(
        "models.User", related_name="subscriptions", null=True, on_delete=fields.CASCADE
    )
