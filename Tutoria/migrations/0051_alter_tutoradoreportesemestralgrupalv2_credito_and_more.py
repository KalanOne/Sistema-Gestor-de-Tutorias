# Generated by Django 4.1.2 on 2022-12-05 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0050_alter_grupo_grupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutoradoreportesemestralgrupalv2',
            name='credito',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tutoradoreportesemestralgrupalv2',
            name='estudianteCanalizado',
            field=models.IntegerField(),
        ),
    ]
