# Generated by Django 4.1.2 on 2022-10-23 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0012_cuestionario_ruta_cuestionariocontestado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuestionariocontestado',
            name='idEstado',
        ),
    ]