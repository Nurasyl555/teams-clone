from django.db import models

# Create your models here.
from typing import Any
from django.contrib.auth.models import (
    AbstractBaseUser,

)
from users.manager import CustomUserManager
from apps.abstract.models import AbstractModel
from models import (
    EmailField,
    CharField,
    BooleanField,
    DateTimeField,

)
class CustomUser(
    AbstractBaseUser,
    AbstractModel
    ):
    emial = EmailField(
        unique=True,
    )
    password = CharField(
        max_length=128,
    )
    first_name = CharField(
        max_length=255,
    )
    last_name = CharField(
        max_length=255,
    )
    is_active = BooleanField(
        default=True,
    )
    is_staff = BooleanField(
        default=False,
    )
    is_superuser = BooleanField(
        default=False,
    )
    date_joined = DateTimeField(
        auto_now_add=True,
    )
    last_login = models.DateTimeField(
        auto_now=True,
    )

USERNAME_FIELD = "email"
REQUIRED_FIELDS = ["first_name", "last_name"]

object = CustomUserManager()
class Meta:
    verbose_name = "user"

def __str__(self):
    return f"Email: {self.email}, Name: {self.first_name} ,Last Name: {self.last_name}"
    

