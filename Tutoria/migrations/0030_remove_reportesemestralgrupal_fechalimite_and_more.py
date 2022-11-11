# Generated by Django 4.1.2 on 2022-11-10 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0029_institucion_anoactual_institucion_periodoactual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportesemestralgrupal',
            name='fechaLimite',
        ),
        migrations.RemoveField(
            model_name='reportesemestralgrupal',
            name='ruta',
        ),
        migrations.AddField(
            model_name='reportesemestralgrupal',
            name='ano',
            field=models.IntegerField(default=2022),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportesemestralgrupal',
            name='archivo',
            field=models.FileField(default='', upload_to='Tutor/ReporteSemestral'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportesemestralgrupal',
            name='periodo',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], default=3),
            preserve_default=False,
        ),
    ]
