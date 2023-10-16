# Generated by Django 4.2.4 on 2023-10-15 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0004_remove_producto_iva_producto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro_diario',
            name='debe',
        ),
        migrations.RemoveField(
            model_name='libro_diario',
            name='haber',
        ),
        migrations.RemoveField(
            model_name='libro_diario',
            name='num_cuenta',
        ),
        migrations.AlterField(
            model_name='libro_diario',
            name='concepto',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='libro_diario',
            name='fecha',
            field=models.DateField(null=True),
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
    ]
