# Generated by Django 4.2.4 on 2023-09-17 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0008_alter_factura_num_factura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='num_factura',
            field=models.CharField(max_length=50),
        ),
    ]
