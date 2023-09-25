# Generated by Django 4.2.4 on 2023-09-24 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0007_remove_producto_descuento_remove_producto_medida_and_more'),
    ]

    operations = [
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
            name='libro_diario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('num_asiento', models.IntegerField()),
                ('concepto', models.CharField(max_length=200)),
                ('debe', models.IntegerField()),
                ('haber', models.IntegerField()),
                ('num_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.cuenta')),
            ],
        ),
    ]
