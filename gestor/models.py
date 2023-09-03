from django.db import models

# Create your models here.
class persona(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

#----------------------------------------------------------------------------------------------------------------------------
    
class Estados(models.Model):
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Dado de baja'),
        ('anulado', 'Factura anulada'),
        ('vigent', 'Factura vigente'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS)

    def __str__(self):
        return self.estado
    
#----------------------------------------------------------------------------------------------------------------------------

class clientes(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    razon_social = models.CharField(max_length=100, null=False)
    RUC = models.CharField(max_length=12)
    direccion = models.CharField(max_length=150)
    correo = models.CharField(max_length=50, null=True)
    num_telefono = models.CharField(max_length=12, null=True)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class proveedor(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    razon_social = models.CharField(max_length=100, null=False)
    RUC = models.CharField(max_length=12)
    direccion = models.CharField(max_length=150)
    correo = models.CharField(max_length=50, null=True)
    num_telefono = models.CharField(max_length=12, null=True)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
#------------------------------------------------------------------------------------------------

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
    descripcion = models.IntegerField()
    color = models.CharField()
    medida = models.CharField()
    descuento = models.IntegerField()
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def __str__(self):
        return self.cod_producto
    
class entrada(models.Model):
    cod_producto = models.ForeignKey(producto, on_delete=models.CASCADE)  
    descripcion = models.IntegerField()
    precio = models.IntegerField()    
    cantidad_entrante = models.IntegerField()

    def __str__(self):
        return self.cantidad_entrante
    
class salida(models.Model):
    fecha_salida = models.DateTimeField()
    cod_producto = models.ForeignKey(producto, on_delete=models.CASCADE)  
    descripcion = models.IntegerField()
    precio = models.IntegerField()    
    cantidad_saliente = models.IntegerField()
    total_venta = models.IntegerField() 

    def __str__(self):
        return self.total_venta
    
class inventario(models.Model):
    cod_producto = models.ForeignKey(producto, on_delete=models.CASCADE)  
    descripcion = models.IntegerField()
    precio = models.IntegerField()  
    entrada = models.IntegerField()
    salida = models.IntegerField()
    existencia = models.IntegerField()

    def __str__(self):
        return self.existencia

#------------------------------------------------------------------------------------------------

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
    cliente = models.ForeignKey(clientes, on_delete=models.CASCADE)
    tipo_factura = models.ForeignKey(tipo_factura, on_delete=models.CASCADE)
    metodo_de_pago = models.ForeignKey(metodo_pago, on_delete=models.CASCADE)
    total_venta = models.IntegerField()
    impuesto_total = models.IntegerField()
    descuento_total = models.IntegerField()
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    def __str__(self):
        return self.num_factura
    
class factura_detalle(models.Model):
    num_factura = models.CharField(max_length=50, null=False)
    cod_producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    precio_unitario = models.IntegerField()
    total_precio = models.IntegerField()
    impuesto = models.IntegerField()
    descuento = models.IntegerField()
    total_precio = models.IntegerField()

    def __str__(self):
        return self.num_factura
