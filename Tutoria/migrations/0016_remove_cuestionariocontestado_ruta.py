# Generated by Django 4.1.2 on 2022-10-24 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0015_remove_cuestionariocontestado_ruta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuestionariocontestado',
            name='ruta',
        ),
    ]
