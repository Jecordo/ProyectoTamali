from django.db import models
from gestor.apps.contable.cuenta.models import cuenta


class libro_diario(models.Model):
    fecha = models.DateField(null=True)
    num_asiento = models.IntegerField()
    concepto = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"Asiento {self.num_asiento} - Fecha: {self.fecha}"


class detalle_libro_diario(models.Model):
    num_asiento = models.ForeignKey(libro_diario, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=200, null=False)
    num_cuenta = models.ForeignKey(cuenta, on_delete=models.CASCADE)
    debe = models.IntegerField()
    haber = models.IntegerField()

    def __str__(self):
        return self.num_asiento

    def to_dict(self):
        return {
            "num_asiento": {
                "concepto": self.num_asiento.concepto,
                "num_asiento": self.num_asiento.num_asiento
            },
            "concepto": self.concepto,
            "num_cuenta": {
                "num_cuenta": self.num_cuenta.num_cuenta,
                "descripcion": self.num_cuenta.descripcion
            },
            "debe": self.debe,
            "haber": self.haber
        }