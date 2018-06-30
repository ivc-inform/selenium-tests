from django.db import models
from django.db.models import Model, TextField


class List(Model):
    # text = TextField(default="")
    ...

class Item(Model):
    text = TextField(default="")
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
