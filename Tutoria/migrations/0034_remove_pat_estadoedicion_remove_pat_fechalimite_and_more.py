# Generated by Django 4.1.2 on 2022-11-13 08:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0033_remove_reportesemestraldepartamento_fechalimite_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pat',
            name='estadoEdicion',
        ),
        migrations.RemoveField(
            model_name='pat',
            name='fechaLimite',
        ),
        migrations.RemoveField(
            model_name='pat',
            name='ruta',
        ),
        migrations.AddField(
            model_name='pat',
            name='ano',
            field=models.IntegerField(default=2022),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pat',
            name='archivo',
            field=models.FileField(default='', upload_to='CoordinadorTutoriaDepartamentoAcademico/PAT'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pat',
            name='fechaEnvio',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pat',
            name='idPersonalTec',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.personaltec'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pat',
            name='periodo',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pat',
            name='idEstado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.estado'),
            preserve_default=False,
        ),
    ]
