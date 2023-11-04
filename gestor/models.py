from django.contrib.auth.models import User
from django.db import models, transaction


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

# ----------------------------------------------------------------------------------------------------------------------------


class Estados(models.Model):
    estado = models.CharField(max_length=10)

    def __str__(self):
        return self.estado

# ----------------------------------------------------------------------------------------------------------------------------


class cliente(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    razon_social = models.CharField(max_length=100, null=False)
    RUC = models.CharField(max_length=12, null=False)
    direccion = models.CharField(max_length=150, null=True)
    correo = models.CharField(max_length=50, null=True)
    num_telefono = models.CharField(max_length=12, null=True)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def __str__(self):
        return self.RUC


class proveedor(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    razon_social = models.CharField(max_length=100, null=False)
    RUC = models.CharField(max_length=12, null=False)
    direccion = models.CharField(max_length=150, null=True)
    correo = models.CharField(max_length=50, null=True)
    num_telefono = models.CharField(max_length=12, null=True)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# ------------------------------------------------------------------------------------------------


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
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def calcular_iva_producto(self):
        return 0.1 * self.precio_venta

    @property
    def iva_producto(self):
        return self.calcular_iva_producto()

    def __str__(self):
        return self.cod_producto


# -------------------------------------------------------------------------------------------


class inventario(models.Model):
    fecha = models.DateTimeField(null=True)
    cod_producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200, null=False)
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
        return f"Stock de {self.producto.nombre}: {self.cantidad}"

# ------------------------------------------------------------------------------------------------


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
    num_factura = models.CharField(max_length=50, null=False)
    timbrado = models.CharField(max_length=50, null=False)
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    tipo_factura = models.ForeignKey(tipo_factura, on_delete=models.CASCADE)
    metodo_de_pago = models.ForeignKey(metodo_pago, on_delete=models.CASCADE)
    total_venta = models.IntegerField(null=True)
    impuesto_total = models.IntegerField(null=True)
    descuento_total = models.IntegerField(null=True)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def __str__(self):
        return self.num_factura


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

# ------------------------------------------------------------------------------------------------------------------------------


class cuenta(models.Model):
    num_cuenta = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=100, null=False)
    saldo = models.IntegerField()

    def __str__(self):
        return self.num_cuenta


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
