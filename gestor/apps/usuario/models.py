from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, null=True)
    apellido = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.user.username