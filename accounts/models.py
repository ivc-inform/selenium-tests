import uuid

from django.db import models

# Create your models here.
from django.db.models import Model, EmailField, CharField


class User(Model):
    email = EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(Model):
    email = EmailField()
    uid = CharField(max_length=40, default=uuid.uuid4)
