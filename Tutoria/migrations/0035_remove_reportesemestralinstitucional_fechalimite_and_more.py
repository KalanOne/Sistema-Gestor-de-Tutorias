# Generated by Django 4.1.2 on 2022-11-13 23:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0034_remove_pat_estadoedicion_remove_pat_fechalimite_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportesemestralinstitucional',
            name='fechaLimite',
        ),
        migrations.RemoveField(
            model_name='reportesemestralinstitucional',
            name='ruta',
        ),
        migrations.AddField(
            model_name='reportesemestralinstitucional',
            name='ano',
            field=models.IntegerField(default=2022),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportesemestralinstitucional',
            name='archivo',
            field=models.FileField(default='', upload_to='CoordinacionInstitucionalTutoria/ReporteSemestral'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportesemestralinstitucional',
            name='fechaEnvio',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportesemestralinstitucional',
            name='idInstitucion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.institucion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportesemestralinstitucional',
            name='periodo',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reportesemestralinstitucional',
            name='idEstado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.estado'),
            preserve_default=False,
        ),
    ]