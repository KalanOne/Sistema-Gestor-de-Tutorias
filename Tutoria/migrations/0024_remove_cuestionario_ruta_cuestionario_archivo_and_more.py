# Generated by Django 4.1.2 on 2022-11-03 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0023_alter_cita_idestado_alter_cita_lugar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuestionario',
            name='ruta',
        ),
        migrations.AddField(
            model_name='cuestionario',
            name='archivo',
            field=models.FileField(default='null', upload_to='Cuestionarios/Asignacion/%Y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cuestionariocontestado',
            name='archivo',
            field=models.FileField(upload_to='Cuestionarios/Respuesta/%Y/%m/%d'),
        ),
    ]
