# Generated by Django 4.1.2 on 2022-10-31 01:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0019_remove_cita_fecha_cita_fechaasignacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='fechaAsignacion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='fechaCita',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='fechaSolicitud',
            field=models.DateField(default=django.utils.timezone.now, editable=False),
        ),
    ]
