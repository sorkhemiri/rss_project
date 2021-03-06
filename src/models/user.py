from uuid import uuid4

from tortoise import fields

from .base import BaseModel


class User(BaseModel):
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    uid = fields.UUIDField(default=uuid4)
    username = fields.CharField(max_length=100, unique=True, required=True, index=True)
    password = fields.CharField(max_length=600, required=True)
    is_admin = fields.BooleanField(default=False)

    def __str__(self):
        return self.username
