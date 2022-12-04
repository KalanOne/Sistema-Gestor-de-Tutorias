# Generated by Django 4.1.2 on 2022-11-28 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0045_cita_idinstitucion'),
    ]

    operations = [
        migrations.CreateModel(
            name='FechaLimite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosticoInstitucional', models.DateField()),
                ('planAccionTutorial', models.DateField()),
                ('programaInstitucionalTutorial', models.DateField()),
                ('reporteSemestralGrupal', models.DateField()),
                ('reporteSemestralDepartamental', models.DateField()),
                ('reporteSemestralInstitucional', models.DateField()),
                ('ano', models.PositiveIntegerField()),
                ('periodo', models.PositiveIntegerField()),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutoria.institucion')),
            ],
            options={
                'verbose_name': 'FechaLimite',
                'verbose_name_plural': 'FechasLimites',
                'db_table': 'fechaLimite',
                'ordering': ['id'],
            },
        ),
        migrations.RemoveField(
            model_name='pat',
            name='idDepartamentoAcademico',
        ),
        migrations.RemoveField(
            model_name='pat',
            name='idEstado',
        ),
        migrations.RemoveField(
            model_name='pat',
            name='idPersonalTec',
        ),
        migrations.RemoveField(
            model_name='pit',
            name='idEstado',
        ),
        migrations.RemoveField(
            model_name='pit',
            name='idInstitucion',
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='idGrupoRespuesta',
        ),
        migrations.RemoveField(
            model_name='reportesemestraldepartamento',
            name='idDepartamentoAcademico',
        ),
        migrations.RemoveField(
            model_name='reportesemestraldepartamento',
            name='idEstado',
        ),
        migrations.RemoveField(
            model_name='reportesemestraldepartamento',
            name='idPersonalTec',
        ),
        migrations.RemoveField(
            model_name='reportesemestralgrupal',
            name='idEstado',
        ),
        migrations.RemoveField(
            model_name='reportesemestralgrupal',
            name='idGrupo',
        ),
        migrations.RemoveField(
            model_name='reportesemestralgrupal',
            name='idPersonalTec',
        ),
        migrations.RemoveField(
            model_name='reportesemestralinstitucional',
            name='idEstado',
        ),
        migrations.RemoveField(
            model_name='reportesemestralinstitucional',
            name='idInstitucion',
        ),
        migrations.RemoveField(
            model_name='reportesemestralinstitucional',
            name='idPersonalTec',
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='idGrupoRespuesta',
        ),
        migrations.RemoveField(
            model_name='respuestacontestada',
            name='idCuestionario',
        ),
        migrations.RemoveField(
            model_name='respuestacontestada',
            name='idPregunta',
        ),
        migrations.RemoveField(
            model_name='respuestacontestada',
            name='idRespuesta',
        ),
        migrations.RemoveField(
            model_name='respuestacontestada',
            name='idTutorado',
        ),
        migrations.DeleteModel(
            name='ConstanciaTutor',
        ),
        migrations.DeleteModel(
            name='GrupoRespuesta',
        ),
        migrations.DeleteModel(
            name='PAT',
        ),
        migrations.DeleteModel(
            name='PIT',
        ),
        migrations.DeleteModel(
            name='Pregunta',
        ),
        migrations.DeleteModel(
            name='ReporteSemestralDepartamento',
        ),
        migrations.DeleteModel(
            name='ReporteSemestralGrupal',
        ),
        migrations.DeleteModel(
            name='ReporteSemestralInstitucional',
        ),
        migrations.DeleteModel(
            name='Respuesta',
        ),
        migrations.DeleteModel(
            name='RespuestaContestada',
        ),
    ]
