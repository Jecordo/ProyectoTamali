from django.db import models

class cuenta(models.Model):
    num_cuenta = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=100, null=False)
    saldo = models.IntegerField()

    def __str__(self):
        return self.num_cuenta