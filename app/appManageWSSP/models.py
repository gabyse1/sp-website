from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

    class Meta:
      verbose_name = "User"
      verbose_name_plural = "Users"
      db_table = "User"
      ordering = ["username"]

    def __str__(self):
      return f"{self.id}: {self.username}, {self.email}, {self.first_name}, {self.last_name}, {self.last_login}"

    def serialize(self):
      if self.last_login:
        lastlog = self.last_login.strftime("%b %d %Y, %I:%M %p")
      else:
        lastlog = None
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "last_login": lastlog
      }