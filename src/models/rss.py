from tortoise import fields
from .base import BaseModel


class RSS(BaseModel):
    title = fields.CharField(max_length=300, required=True)
    link = fields.CharField(max_length=500, required=True)
    description = fields.CharField(max_length=500)
    source = fields.ForeignKeyField('models.RSSSource', related_name='rss_content', null=True, on_delete=fields.SET_NULL)
    pub_date = fields.DateField(null=True)

    def __str__(self):
        return self.title
