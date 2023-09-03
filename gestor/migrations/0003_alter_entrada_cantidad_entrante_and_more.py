# Generated by Django 4.2.4 on 2023-09-03 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0002_categoria_clientes_estados_marca_metodo_pago_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='cantidad_entrante',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='descripcion',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='precio',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='factura',
            name='descuento_total',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='factura',
            name='impuesto_total',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='factura',
            name='total_venta',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='factura_detalle',
            name='descuento',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='factura_detalle',
            name='impuesto',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='factura_detalle',
            name='precio_unitario',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='factura_detalle',
            name='total_precio',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='descripcion',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='entrada',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='existencia',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='precio',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='salida',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='producto',
            name='color',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descuento',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='producto',
            name='medida',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_costo',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_venta',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='salida',
            name='cantidad_saliente',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='salida',
            name='descripcion',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='salida',
            name='precio',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='salida',
            name='total_venta',
            field=models.IntegerField(),
        ),
    ]
