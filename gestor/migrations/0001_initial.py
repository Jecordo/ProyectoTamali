# Generated by Django 4.2.4 on 2023-11-03 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('apellido', models.CharField(max_length=50, null=True)),
                ('razon_social', models.CharField(max_length=100)),
                ('RUC', models.CharField(max_length=12)),
                ('direccion', models.CharField(max_length=150, null=True)),
                ('correo', models.CharField(max_length=50, null=True)),
                ('num_telefono', models.CharField(max_length=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_cuenta', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('saldo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Estados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_factura', models.CharField(max_length=50)),
                ('timbrado', models.CharField(max_length=50)),
                ('total_venta', models.IntegerField(null=True)),
                ('impuesto_total', models.IntegerField(null=True)),
                ('descuento_total', models.IntegerField(null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.cliente')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.estados')),
            ],
        ),
        migrations.CreateModel(
            name='libro_diario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True)),
                ('num_asiento', models.IntegerField()),
                ('concepto', models.CharField(max_length=200, null=True)),
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
                ('precio_costo', models.IntegerField()),
                ('precio_venta', models.IntegerField()),
                ('descripcion', models.CharField(max_length=200)),
                ('cod_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.categoria')),
                ('cod_marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.marca')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
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
            name='stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.producto')),
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
                ('direccion', models.CharField(max_length=150, null=True)),
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
            name='libro_mayor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('num_asiento', models.IntegerField()),
                ('concepto', models.CharField(max_length=200)),
                ('debe', models.IntegerField()),
                ('haber', models.IntegerField()),
                ('saldo', models.IntegerField()),
                ('num_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.cuenta')),
            ],
        ),
        migrations.CreateModel(
            name='inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(null=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('tipo_movimiento', models.BooleanField()),
                ('cantidad', models.BooleanField()),
                ('cod_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.producto')),
            ],
        ),
        migrations.CreateModel(
            name='factura_detalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.IntegerField(null=True)),
                ('total_precio', models.IntegerField()),
                ('impuesto', models.IntegerField(null=True)),
                ('descuento', models.IntegerField(null=True)),
                ('cod_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.producto')),
                ('num_factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.factura')),
            ],
        ),
        migrations.AddField(
            model_name='factura',
            name='metodo_de_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.metodo_pago'),
        ),
        migrations.AddField(
            model_name='factura',
            name='tipo_factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.tipo_factura'),
        ),
        migrations.CreateModel(
            name='detalle_libro_diario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concepto', models.CharField(max_length=200)),
                ('debe', models.IntegerField()),
                ('haber', models.IntegerField()),
                ('num_asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.libro_diario')),
                ('num_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.cuenta')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, null=True)),
                ('apellido', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.estados'),
        ),
    ]
