# Generated by Django 4.1.2 on 2022-10-17 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0008_orden_alter_cuestionario_idestado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='descripcion',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='horaCanalizacion',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='horaFinal',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='horaInicio',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='idPersonalMed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.personalmed'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='idPersonalTec',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.personaltec'),
        ),
    ]
