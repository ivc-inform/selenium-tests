from django.db import models
from django.db.models import Model, TextField
from django.urls import reverse

from project import settings


class List(Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=None)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(Model):
    text = TextField(default="")
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
