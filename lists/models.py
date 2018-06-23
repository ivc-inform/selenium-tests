from django.db import models
from django.db.models import Model, TextField


class Item(Model):
    text = TextField(default="")
