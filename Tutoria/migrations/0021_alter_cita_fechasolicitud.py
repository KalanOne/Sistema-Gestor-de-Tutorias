# Generated by Django 4.1.2 on 2022-10-31 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0020_alter_cita_fechaasignacion_alter_cita_fechacita_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='fechaSolicitud',
            field=models.DateField(auto_now_add=True),
        ),
    ]