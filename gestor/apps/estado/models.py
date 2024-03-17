import datetime
from django.db import models


class estado(models.Model):
    estado = models.CharField(max_length=10)

    def __str__(self):
        return self.estado
