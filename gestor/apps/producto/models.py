from django.db import models
from gestor.apps.proveedor.models import proveedor
from gestor.apps.estado.models import estado


class categoria(models.Model):
    descripcion = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.descripcion


class marca(models.Model):
    descripcion = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.descripcion


class producto(models.Model):
    cod_producto = models.CharField(max_length=50, null=False)
    cod_proveedor = models.ForeignKey(proveedor, on_delete=models.CASCADE)
    cod_categoria = models.ForeignKey(categoria, on_delete=models.CASCADE)
    cod_marca = models.ForeignKey(marca, on_delete=models.CASCADE)
    precio_costo = models.IntegerField()
    precio_venta = models.IntegerField()
    descripcion = models.CharField(max_length=200, null=False)
    estado = models.ForeignKey(estado, on_delete=models.CASCADE)

    def calcular_iva_producto(self):
        return 0.1 * self.precio_venta

    @property
    def iva_producto(self):
        return self.calcular_iva_producto()

    def __str__(self):
        return self.cod_producto

