# Generated by Django 4.1.2 on 2022-11-03 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0024_remove_cuestionario_ruta_cuestionario_archivo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuestionario',
            name='idEstado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.estado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cuestionario',
            name='idGrupo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.grupo'),
            preserve_default=False,
        ),
    ]
