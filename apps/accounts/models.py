from typing import List

from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    password_expire_at = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.email
