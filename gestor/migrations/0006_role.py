# Generated by Django 4.2.4 on 2023-10-23 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0005_remove_libro_diario_debe_remove_libro_diario_haber_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]