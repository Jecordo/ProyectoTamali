import datetime
from django.contrib.auth.models import User
from django.db import models, transaction
from gestor.apps.estado.models import estado


class proveedor(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    razon_social = models.CharField(max_length=100, null=False)
    RUC = models.CharField(max_length=12, null=False)
    direccion = models.CharField(max_length=150, null=True)
    correo = models.CharField(max_length=50, null=True)
    num_telefono = models.CharField(max_length=12, null=True)
    estado = models.ForeignKey(estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


