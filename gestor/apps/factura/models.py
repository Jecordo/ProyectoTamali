import datetime
from django.db import models
from gestor.apps.cliente.models import cliente
from gestor.apps.producto.models import producto
from gestor.apps.estado.models import estado




class tipo_factura(models.Model):
    ESTADOS = (
        ('credit', 'Credito'),
        ('cont', 'Contado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS)

    def __str__(self):
        return self.estado


class metodo_pago(models.Model):
    descripcion = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.descripcion


class factura(models.Model):
    fecha = models.DateTimeField(null=True)
    num_factura = models.CharField(max_length=50, null=False)
    timbrado = models.CharField(max_length=50, null=False)
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    tipo_factura = models.ForeignKey(tipo_factura, on_delete=models.CASCADE)
    metodo_de_pago = models.ForeignKey(metodo_pago, on_delete=models.CASCADE)
    total_venta = models.IntegerField(null=True)
    impuesto_total = models.IntegerField(null=True)
    descuento_total = models.IntegerField(null=True)
    estado = models.ForeignKey(estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.num_factura
    
    def guardar_fecha(self, year, month, day):
        # Crea un objeto datetime con los valores proporcionados
        fecha_obj = datetime(year, month, day)


class factura_detalle(models.Model):
    num_factura = models.ForeignKey(factura, on_delete=models.CASCADE)
    cod_producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField(null=True)
    total_precio = models.IntegerField()
    impuesto = models.IntegerField(null=True)
    descuento = models.IntegerField(null=True)

    def __str__(self):
        return self.num_factura


class detalle_temp(models.Model):
    num_factura = models.ForeignKey(factura, on_delete=models.CASCADE)
    cod_producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField(null=True)
    total_precio = models.IntegerField()
    impuesto = models.IntegerField(null=True)
    descuento = models.IntegerField(null=True)

    def __str__(self):
        return self.num_factura

