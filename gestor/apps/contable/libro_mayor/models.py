from django.db import models
from gestor.apps.contable.cuenta.models import cuenta


class libro_mayor(models.Model):
    fecha = models.DateField()
    num_asiento = models.IntegerField()
    concepto = models.CharField(max_length=200, null=False)
    num_cuenta = models.ForeignKey(cuenta, on_delete=models.CASCADE)
    debe = models.IntegerField()
    haber = models.IntegerField()
    saldo = models.IntegerField()

    def __str__(self):
        return self.num_asiento

    def __str__(self):
        return self.saldo

    def __str__(self):
        return self.num_cuenta
