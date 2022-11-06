# Generated by Django 4.1.2 on 2022-10-31 00:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0018_alter_cuestionariocontestado_archivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cita',
            name='fecha',
        ),
        migrations.AddField(
            model_name='cita',
            name='fechaAsignacion',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cita',
            name='fechaCita',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cita',
            name='fechaSolicitud',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]