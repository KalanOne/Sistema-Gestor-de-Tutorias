# Generated by Django 4.1.2 on 2022-12-07 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0051_alter_tutoradoreportesemestralgrupalv2_credito_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutoradoreportesemestralgrupalv2',
            name='tutoriaGrupal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tutoradoreportesemestralgrupalv2',
            name='tutoriaIndividual',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tutorreportesemestraldepartamentalv2',
            name='estudianteCanalizado',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tutorreportesemestraldepartamentalv2',
            name='tutoriaGrupal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tutorreportesemestraldepartamentalv2',
            name='tutoriaIndividual',
            field=models.IntegerField(),
        ),
    ]