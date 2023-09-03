# Generated by Django 4.2.4 on 2023-08-31 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('apellido', models.CharField(max_length=50, null=True)),
                ('razon_social', models.CharField(max_length=100)),
                ('RUC', models.CharField(max_length=12)),
                ('direccion', models.CharField(max_length=150)),
                ('correo', models.CharField(max_length=50, null=True)),
                ('num_telefono', models.CharField(max_length=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Dado de baja'), ('anulado', 'Factura anulada'), ('vigent', 'Factura vigente')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='metodo_pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_producto', models.CharField(max_length=50)),
                ('precio_costo', models.IntegerField(max_length=250)),
                ('precio_venta', models.IntegerField(max_length=250)),
                ('descripcion', models.IntegerField(max_length=500)),
                ('color', models.IntegerField(max_length=20)),
                ('medida', models.IntegerField(max_length=20)),
                ('descuento', models.IntegerField(max_length=2)),
                ('cod_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.categoria')),
                ('cod_marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.marca')),
            ],
        ),
        migrations.CreateModel(
            name='tipo_factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('credit', 'Credito'), ('cont', 'Contado')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='salida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_salida', models.DateTimeField()),
                ('descripcion', models.IntegerField(max_length=500)),
                ('precio', models.IntegerField(max_length=250)),
                ('cantidad_saliente', models.IntegerField(max_length=50)),
                ('total_venta', models.IntegerField(max_length=250)),
                ('cod_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.producto')),
            ],
        ),
        migrations.CreateModel(
            name='proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('apellido', models.CharField(max_length=50, null=True)),
                ('razon_social', models.CharField(max_length=100)),
                ('RUC', models.CharField(max_length=12)),
                ('direccion', models.CharField(max_length=150)),
                ('correo', models.CharField(max_length=50, null=True)),
                ('num_telefono', models.CharField(max_length=12, null=True)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.estados')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='cod_proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.proveedor'),
        ),
        migrations.AddField(
            model_name='producto',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.estados'),
        ),
        migrations.CreateModel(
            name='inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.IntegerField(max_length=500)),
                ('precio', models.IntegerField(max_length=250)),
                ('entrada', models.IntegerField(max_length=50)),
                ('salida', models.IntegerField(max_length=50)),
                ('existencia', models.IntegerField(max_length=50)),
                ('cod_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.producto')),
            ],
        ),
        migrations.CreateModel(
            name='factura_detalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_factura', models.CharField(max_length=50)),
                ('precio_unitario', models.IntegerField(max_length=250)),
                ('impuesto', models.IntegerField(max_length=2)),
                ('descuento', models.IntegerField(max_length=2)),
                ('total_precio', models.IntegerField(max_length=250)),
                ('cod_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.producto')),
            ],
        ),
        migrations.CreateModel(
            name='factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_factura', models.CharField(max_length=50)),
                ('total_venta', models.IntegerField(max_length=250)),
                ('impuesto_total', models.IntegerField(max_length=2)),
                ('descuento_total', models.IntegerField(max_length=2)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.clientes')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.estados')),
                ('metodo_de_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.metodo_pago')),
                ('tipo_factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.tipo_factura')),
            ],
        ),
        migrations.CreateModel(
            name='entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.IntegerField(max_length=500)),
                ('precio', models.IntegerField(max_length=250)),
                ('cantidad_entrante', models.IntegerField(max_length=50)),
                ('cod_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.producto')),
            ],
        ),
        migrations.AddField(
            model_name='clientes',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.estados'),
        ),
    ]
