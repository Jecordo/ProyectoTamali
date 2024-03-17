import datetime
from django.contrib.auth.models import User
from django.db import models, transaction
from gestor.apps.producto.models import producto


class inventario(models.Model):
    fecha = models.DateTimeField(null=True)
    cod_producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200, null=False)
    referencia = models.CharField(max_length=200, null=True)
    tipo_movimiento = models.BooleanField()
    cantidad = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)  # Guarda el objeto inventario

            # Actualiza el stock según el tipo de movimiento
            if self.tipo_movimiento:  # Si es True (entrada)
                stock_obj, created = stock.objects.get_or_create(
                    producto=self.cod_producto)
                stock_obj.cantidad += int(self.cantidad)
                stock_obj.save()
            else:  # Si es False (salida)
                try:
                    stock_obj = stock.objects.get(producto=self.cod_producto)
                    stock_obj.cantidad -= int(self.cantidad)
                    stock_obj.save()
                except stock.DoesNotExist:
                    # Maneja el caso en el que no se encuentra el registro de stock
                    pass

    def __str__(self):
        return self.cantidad


class stock(models.Model):
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return self.cantidad

