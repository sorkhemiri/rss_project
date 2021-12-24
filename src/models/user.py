from tortoise import fields

from .base import BaseModel


class User(BaseModel):
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    username = fields.CharField(max_length=100, unique=True, required=True, index=True)
    password = fields.CharField(max_length=600, required=True)

    def __str__(self):
        return self.username
